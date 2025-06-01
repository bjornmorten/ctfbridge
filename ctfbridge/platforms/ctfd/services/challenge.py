"""CTFd challenge service implementation"""

import logging
from typing import List, Optional

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

logger = logging.getLogger(__name__)


class CTFdChallengeService(CoreChallengeService):
    """Service for interacting with CTFd challenge endpoints"""

    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return False

    def _handle_common_errors(self, response, challenge_id: Optional[str] = None) -> None:
        """Handle common CTFd error responses."""
        location = response.headers.get("location", "")
        if response.status_code == 401 or (response.status_code == 302 and "login" in location):
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

            data = response.json()
            challenges = [CTFdChallenge(**chal) for chal in data.get("data", [])]
            return [challenge.to_core_model() for challenge in challenges]

        except (NotAuthenticatedError, ChallengesUnavailableError):
            raise
        except Exception as e:
            logger.debug("Error while fetching or parsing challenges", exc_info=e)
            raise ChallengeFetchError("Failed to fetch or parse challenges from CTFd") from e

    async def _fetch_challenge_by_id(self, challenge_id: str) -> Challenge:
        """Fetch a single challenge by ID."""
        try:
            url = Endpoints.Challenges.detail(id=challenge_id)
            response = await self._client.get(url)
            self._handle_common_errors(response, challenge_id)

            data = response.json()
            challenge = CTFdChallenge(**data.get("data", {}))
            return challenge.to_core_model()

        except (NotAuthenticatedError, ChallengesUnavailableError, ChallengeNotFoundError):
            raise
        except Exception as e:
            logger.debug("Error while fetching or parsing challenge %s", challenge_id, exc_info=e)
            raise ChallengeFetchError(
                f"Failed to fetch or parse challenge {challenge_id} from CTFd"
            ) from e

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        """Submit a flag for a challenge."""
        try:
            response = await self._client.post(
                Endpoints.Challenges.SUBMIT,
                json={"challenge_id": challenge_id, "submission": flag},
            )
            self._handle_common_errors(response, challenge_id)

            data = response.json()
            submission = CTFdSubmission(**data.get("data", {}))
            return submission.to_core_model()

        except (NotAuthenticatedError, ChallengeNotFoundError, ChallengesUnavailableError):
            raise
        except Exception as e:
            logger.debug("Error while submitting flag for challenge %s", challenge_id, exc_info=e)
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Failed to submit flag"
            ) from e
