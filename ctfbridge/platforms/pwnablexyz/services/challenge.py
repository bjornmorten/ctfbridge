import logging
from typing import List

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions.challenge import ChallengeFetchError
from ctfbridge.models.challenge import Challenge
from ctfbridge.platforms.pwnablexyz.utils.parsers import parse_challenges
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.exceptions import SubmissionError

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class PwnableXYZChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return True

    async def _fetch_challenges(self) -> List[Challenge]:
        try:
            response = await self._client.get("/challenges/")
            response.raise_for_status()
            challenges = parse_challenges(response.text)
            return challenges
        except Exception as e:
            logger.debug("Error while fetching or parsing challenges", exc_info=e)
            raise ChallengeFetchError("Failed to fetch or parse challenges from pwnable.xyz") from e

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        try:
            resp = await self._client.get("/challenges/")
            soup = BeautifulSoup(resp.text, "html.parser")
            csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"}).get("value")
            logger.debug("Got CSRF token %s", csrf_token)

            response = await self._client.post(
                f"/challenges/{challenge_id}/",
                data={"csrfmiddlewaretoken": csrf_token, "id": challenge_id, "flag": flag},
                headers={"Referer": "https://pwnable.xyz/"},
                follow_redirects=True,
            )

            correct = "solve.Success()" in response.text
            return SubmissionResult(correct=correct, message="correct" if correct else "incorrect")
        except Exception as e:
            logger.debug("Error while submitting flag for challenge %s", challenge_id, exc_info=e)
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Failed to submit flag"
            ) from e
