import logging
import re

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions.challenge import ChallengeFetchError
from ctfbridge.models.challenge import Challenge
from ctfbridge.platforms.pwnablekr.utils.parsers import parse_challenges, parse_challenge_detail
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.exceptions import SubmissionError

logger = logging.getLogger(__name__)


class PwnableKRChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

        self._base_challenges_cache = None

    @property
    def base_has_details(self) -> bool:
        return False

    async def _fetch_challenges(self) -> list[Challenge]:
        try:
            response = await self._client.get("/play.php")
            response.raise_for_status()
            challenges = parse_challenges(response.text)
            self._base_challenges_cache = challenges
            return challenges
        except Exception as e:
            logger.debug("Error while fetching or parsing challenges", exc_info=e)
            raise ChallengeFetchError("Failed to fetch or parse challenges from pwnable.kr") from e

    async def _fetch_challenge_by_id(self, challenge_id: str) -> Challenge:
        try:
            response = await self._client.get("/playproc.php", params={"id": challenge_id})
            response.raise_for_status()
            base_challenge = next(
                chal for chal in self._base_challenges_cache if chal.id == challenge_id
            )
            challenge = parse_challenge_detail(base_challenge, response.text)
            return challenge
        except Exception as e:
            logger.debug("Error while fetching or parsing challenge %s", challenge_id, exc_info=e)
            raise ChallengeFetchError(
                f"Failed to fetch or parse challenge {challenge_id} from pwnable.kr"
            ) from e

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        try:
            response = await self._client.post(
                "/lib.php", params={"cmd": "auth"}, data={"flag": flag}
            )
            msg = re.search(r"alert\('([^']+)'\)", response.text).group(1)
            return SubmissionResult(correct="Congratz" in msg, message=msg)
        except Exception as e:
            logger.debug("Error while submitting flag for challenge %s", challenge_id, exc_info=e)
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Failed to submit flag"
            ) from e
