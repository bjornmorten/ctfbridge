"""CTFd challenge service"""

import logging
from typing import List

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions.challenge import (
    ChallengeFetchError,
    SubmissionError,
    ChallengeNotFoundError,
    ChallengesUnavailableError,
)
from ctfbridge.exceptions.auth import NotAuthenticatedError
from ctfbridge.models.challenge import Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.platforms.ctfd.http.endpoints import Endpoints
from ctfbridge.platforms.ctfd.parsers.challenge_parser import parse_ctfd_challenge
from ctfbridge.platforms.ctfd.utils.csrf import extract_csrf_nonce

logger = logging.getLogger(__name__)


class CTFdChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return False

    def _handle_common_errors(self, response, challenge_id: str = None):
        if response.status_code == 401 or (
            response.status_code == 302 and "login" in response.headers.get("location", "")
        ):
            raise NotAuthenticatedError()
        if response.status_code == 403:
            raise ChallengesUnavailableError()
        if response.status_code == 404 and challenge_id is not None:
            raise ChallengeNotFoundError(challenge_id)

    def _safe_json(self, response, error_cls, context: str, *args):
        try:
            return response.json()
        except Exception as e:
            logger.debug(f"Invalid JSON while {context}", exc_info=e)
            raise error_cls(*args) from e

    async def _get_csrf_token(self) -> str:
        try:
            response = await self._client.get(Endpoints.Misc.BASE_PAGE)
            csrf_token = extract_csrf_nonce(response.text)
            if not csrf_token:
                raise ValueError("Missing CSRF token")
            return csrf_token
        except Exception as e:
            logger.debug("CSRF token retrieval failed", exc_info=e)
            raise

    async def _fetch_challenges(self) -> List[Challenge]:
        try:
            response = await self._client.get(Endpoints.Challenges.LIST)
        except Exception as e:
            logger.debug("Network error while fetching challenges", exc_info=e)
            raise ChallengeFetchError("Network error while fetching challenges from CTFd.") from e

        self._handle_common_errors(response)

        data = self._safe_json(
            response,
            ChallengeFetchError,
            "parsing challenges",
            "Invalid JSON while fetching challenges from CTFd.",
        )

        try:
            return [parse_ctfd_challenge(chal) for chal in data.get("data", [])]
        except Exception as e:
            logger.debug("Failed to parse challenge data", exc_info=e)
            raise ChallengeFetchError("Failed to parse challenge data from CTFd.") from e

    async def _fetch_challenge_by_id(self, challenge_id: str) -> Challenge:
        try:
            url = Endpoints.Challenges.detail(id=challenge_id)
            response = await self._client.get(url)
        except Exception as e:
            logger.debug("Network error while fetching challenge ID %s", challenge_id, exc_info=e)
            raise ChallengeFetchError(
                f"Network error while fetching challenge ID {challenge_id} from CTFd."
            ) from e

        self._handle_common_errors(response, challenge_id)

        data = self._safe_json(
            response,
            ChallengeFetchError,
            f"parsing challenge ID {challenge_id}",
            f"Invalid JSON while fetching challenge ID {challenge_id} from CTFd.",
        )

        try:
            return parse_ctfd_challenge(data.get("data", {}))
        except Exception as e:
            logger.debug("Failed to parse challenge data for ID %s", challenge_id, exc_info=e)
            raise ChallengeFetchError(
                f"Failed to parse challenge data for ID {challenge_id} from CTFd."
            ) from e

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        headers = {}

        if "authorization" not in self._client._http.headers:
            try:
                headers["CSRF-Token"] = await self._get_csrf_token()
            except Exception:
                raise SubmissionError(
                    challenge_id=challenge_id, flag=flag, reason="Failed to fetch CSRF token"
                )

        payload = {"challenge_id": challenge_id, "submission": flag}
        try:
            response = await self._client.post(
                Endpoints.Challenges.SUBMIT, json=payload, headers=headers
            )
        except Exception as e:
            logger.debug("POST request to submit flag failed", exc_info=e)
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Network error during submission"
            ) from e

        if response.status_code in (401, 403):
            if response.headers.get("content-type") == "application/json":
                try:
                    msg = response.json().get("message")
                    if msg:
                        raise NotAuthenticatedError(msg)
                except Exception:
                    pass
            raise NotAuthenticatedError()

        if response.status_code == 404:
            raise ChallengeNotFoundError(challenge_id)

        try:
            data = response.json().get("data", {})
        except Exception as e:
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Invalid JSON in response"
            ) from e

        status = data.get("status")
        message = data.get("message", "No message provided.")
        if status is None:
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Missing 'status' in response"
            )

        return SubmissionResult(correct=(status.lower() == "correct"), message=message)
