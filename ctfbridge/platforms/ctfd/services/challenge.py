"""CTFd challenge service implementation"""

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
from ctfbridge.platforms.ctfd.models.challenge import CTFdChallenge, CTFdSubmission
from ctfbridge.platforms.ctfd.utils.csrf import get_csrf_nonce
from ctfbridge.models.auth import AuthMethod

logger = logging.getLogger(__name__)


class CTFdChallengeService(CoreChallengeService):
    """Service for interacting with CTFd challenge endpoints"""

    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return False

    def _handle_common_errors(self, response, challenge_id: str | None = None):
        """Handle common CTFd error responses."""
        if response.status_code == 401 or (
            response.status_code == 302 and "login" in response.headers.get("location", "")
        ):
            raise NotAuthenticatedError()
        if response.status_code == 403:
            raise ChallengesUnavailableError()
        if response.status_code == 404 and challenge_id is not None:
            raise ChallengeNotFoundError(challenge_id)

    async def _fetch_challenges(self) -> List[Challenge]:
        """Fetch list of all challenges."""
        try:
            response = await self._client.get(Endpoints.Challenges.LIST)
            self._handle_common_errors(response)

            try:
                data = response.json()
                challenges = [CTFdChallenge(**chal) for chal in data.get("data", [])]
                return [challenge.to_core_model() for challenge in challenges]
            except Exception as e:
                logger.debug("Failed to parse challenge data", exc_info=e)
                raise ChallengeFetchError("Failed to parse challenge data from CTFd") from e

        except NotAuthenticatedError:
            raise
        except ChallengesUnavailableError:
            raise
        except Exception as e:
            logger.debug("Failed to fetch challenges", exc_info=e)
            raise ChallengeFetchError("Failed to fetch challenges from CTFd") from e

    async def _fetch_challenge_by_id(self, challenge_id: str) -> Challenge:
        """Fetch a single challenge by ID."""
        try:
            url = Endpoints.Challenges.detail(id=challenge_id)
            response = await self._client.get(url)
            self._handle_common_errors(response, challenge_id)

            try:
                data = response.json()
                challenge = CTFdChallenge(**data.get("data", {}))
                return challenge.to_core_model()
            except Exception as e:
                logger.debug("Failed to parse challenge data for ID %s", challenge_id, exc_info=e)
                raise ChallengeFetchError(
                    f"Failed to parse challenge {challenge_id} from CTFd"
                ) from e

        except (NotAuthenticatedError, ChallengesUnavailableError, ChallengeNotFoundError):
            raise
        except Exception as e:
            logger.debug("Failed to fetch challenge %s", challenge_id, exc_info=e)
            raise ChallengeFetchError(f"Failed to fetch challenge {challenge_id} from CTFd") from e

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        """Submit a flag for a challenge."""
        try:
            headers = {}

            if self._client.auth.active_auth_method in [AuthMethod.CREDENTIALS, AuthMethod.COOKIES]:
                headers["CSRF-Token"] = await get_csrf_nonce(self._client)

            response = await self._client.post(
                Endpoints.Challenges.SUBMIT,
                json={"challenge_id": challenge_id, "submission": flag},
                headers=headers,
            )

            self._handle_common_errors(response, challenge_id)

            try:
                data = response.json()
                submission = CTFdSubmission(**data.get("data", {}))
                return submission.to_core_model()
            except Exception as e:
                logger.debug("Failed to parse submission response", exc_info=e)
                raise SubmissionError(
                    challenge_id=challenge_id, flag=flag, reason="Invalid response format"
                ) from e

        except (NotAuthenticatedError, ChallengeNotFoundError, ChallengesUnavailableError):
            raise
        except Exception as e:
            logger.debug("Failed to submit flag", exc_info=e)
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Failed to submit flag"
            ) from e
