import logging
from typing import List

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions.challenge import ChallengeFetchError, SubmissionError
from ctfbridge.models.challenge import Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.platforms.ctfd.parser import parse_ctfd_challenge
from ctfbridge.platforms.ctfd.utils import extract_csrf_nonce
from ctfbridge.processors.enrich import enrich_challenge

logger = logging.getLogger(__name__)


class CTFdChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return False

    async def _fetch_challenges(self) -> List[Challenge]:
        try:
            response = await self._client.get("challenges")
            data = response.json()
            return [parse_ctfd_challenge(chal) for chal in data.get("data", [])]
        except Exception as e:
            logger.exception("Failed to fetch challenges")
            raise ChallengeFetchError("Failed to fetch challenges from CTFd.") from e

    async def _fetch_challenge_by_id(self, challenge_id: str, enrich: bool = True) -> Challenge:
        try:
            response = await self._client.get("challenge", id=challenge_id)
            data = response.json()
            challenge = parse_ctfd_challenge(data.get("data", {}))
            return enrich_challenge(challenge) if enrich else challenge
        except Exception as e:
            logger.exception("Failed to fetch challenge ID %s", challenge_id)
            raise ChallengeFetchError(f"Could not load challenge ID {challenge_id}") from e

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        try:
            response = await self._client.get("base_page")
            csrf_token = extract_csrf_nonce(response.text)

            if not csrf_token:
                raise SubmissionError(
                    challenge_id=challenge_id, flag=flag, reason="Missing CSRF token"
                )

            response = await self._client.post(
                "submit",
                json={"challenge_id": challenge_id, "submission": flag},
                headers={"CSRF-Token": csrf_token},
            )

            result = response.json().get("data", {})
            status = result.get("status")
            message = result.get("message", "No message provided.")
            if status is None:
                raise SubmissionError(
                    challenge_id=challenge_id, flag=flag, reason="Missing 'status' in response"
                )

            return SubmissionResult(correct=(status == "correct"), message=message)
        except Exception as e:
            logger.exception("Flag submission failed")
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Submission failed"
            ) from e
