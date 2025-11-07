"""EPT challenge service implementation"""

import logging
from httpx import HTTPError
from typing import List

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions import SubmissionError, CTFInactiveError
from ctfbridge.exceptions.challenge import ChallengeFetchError
from ctfbridge.models.challenge import Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.platforms.ept.http.endpoints import Endpoints
from ctfbridge.platforms.ept.models.challenge import EPTChallenge, EPTSubmission

logger = logging.getLogger(__name__)


class EPTChallengeService(CoreChallengeService):
    """Service for interacting with EPT challenge endpoints"""

    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return True

    async def _fetch_challenges(self) -> List[Challenge]:
        try:
            response = await self._client.get(Endpoints.Challenges.LIST)
            data = response.json()

            self._check_detail_response(data)

            if not isinstance(data, list):
                logger.warning("Unexpected response format for challenges: %s", data)
                raise ChallengeFetchError("Unexpected response format from EPT")

            challenges = [EPTChallenge(**chal) for chal in data]
            logger.info("Fetched %d challenges from EPT", len(challenges))
            return [challenge.to_core_model() for challenge in challenges]

        except CTFInactiveError:
            raise
        except HTTPError as e:
            logger.error("HTTP error while fetching challenges", exc_info=e)
            raise ChallengeFetchError("Failed to reach EPT challenge endpoint") from e
        except Exception as e:
            logger.exception("Error while fetching or parsing challenges")
            raise ChallengeFetchError("Failed to fetch or parse challenges from EPT") from e

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        try:
            response = await self._client.post(
                Endpoints.Challenges.submit_flag(id=challenge_id), json={"flag": flag}
            )
            data = response.json()

            self._check_detail_response(data)

            submission = EPTSubmission(**data)
            return submission.to_core_model()

        except CTFInactiveError:
            raise
        except HTTPError as e:
            logger.error(
                "HTTP error while submitting flag for challenge %s", challenge_id, exc_info=e
            )
            raise SubmissionError(
                challenge_id=challenge_id,
                flag=flag,
                reason="Failed to reach EPT challenge endpoint",
            ) from e
        except Exception as e:
            logger.exception("Error while submitting flag for challenge %s", challenge_id)
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Failed to submit flag"
            ) from e

    @staticmethod
    def _check_detail_response(data):
        if not isinstance(data, list):
            detail = data.get("detail")
            if detail == "The CTF has not started yet!":
                raise CTFInactiveError(detail)
