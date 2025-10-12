import logging
from typing import List

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions.challenge import ChallengeFetchError
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.models.challenge import Challenge
from ctfbridge.exceptions import SubmissionError, NotAuthenticatedError
from ctfbridge.exceptions.challenge import ChallengeNotFoundError
from ctfbridge.platforms.pwnabletw.utils.parsers import parse_challenges

logger = logging.getLogger(__name__)


class PwnableTWChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return True

    async def _fetch_challenges(self) -> List[Challenge]:
        try:
            response = await self._client.get("/challenge/")
            response.raise_for_status()
            challenges = parse_challenges(response.text)
            return challenges
        except Exception as e:
            logger.debug("Error while fetching or parsing challenges", exc_info=e)
            raise ChallengeFetchError("Failed to fetch or parse challenges from pwnable.tw") from e

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        try:
            response = await self._client.post(
                "/challenge/submit_flag",
                data={"id": challenge_id, "flag": flag},
            )
            data = response.json()
            return SubmissionResult(correct=str(data) == challenge_id, message=str(data))
        except (NotAuthenticatedError, ChallengeNotFoundError):
            raise
        except Exception as e:
            logger.debug("Error while submitting flag for challenge %s", challenge_id, exc_info=e)
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Failed to submit flag"
            ) from e
