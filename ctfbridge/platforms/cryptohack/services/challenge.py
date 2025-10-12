import logging
from typing import List
import asyncio

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions.challenge import ChallengeFetchError
from ctfbridge.models.challenge import Challenge
from ctfbridge.platforms.cryptohack.http.endpoints import Endpoints
from ctfbridge.platforms.cryptohack.utils.parsers import parse_challenges, parse_categories
from ctfbridge.platforms.cryptohack.utils.csrf import get_csrf_token
from ctfbridge.platforms.cryptohack.models.challenge import CryptoHackChallenge, CryptoHackCategory
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.exceptions import SubmissionError, NotAuthenticatedError
from ctfbridge.exceptions.challenge import ChallengeNotFoundError

logger = logging.getLogger(__name__)


class CryptoHackChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return True

    async def _fetch_challenges(self) -> List[Challenge]:
        try:
            response = await self._client.get(Endpoints.Challenges.CATEGORIES)
            response.raise_for_status()

            categories: List[CryptoHackCategory] = parse_categories(response.text)

            if self._client.category_from_url:
                categories = [
                    c
                    for c in categories
                    if c.path == f"/challenges/{self._client.category_from_url}/"
                ]

            async def fetch_category(category: CryptoHackCategory):
                try:
                    res = await self._client.get(
                        Endpoints.Challenges.category_challenges(category.path)
                    )
                    res.raise_for_status()
                    challenges = parse_challenges(res.text)
                    return challenges
                except Exception as inner_e:
                    logger.warning(f"Failed to fetch category {category.name}: {inner_e}")
                    return []

            results = await asyncio.gather(
                *(fetch_category(cat) for cat in categories),
                return_exceptions=False,
            )

            challenges: List[CryptoHackChallenge] = [c for group in results for c in group]

            return [challenge.to_core_model() for challenge in challenges]

        except Exception as e:
            logger.debug("Error while fetching or parsing challenges", exc_info=e)
            raise ChallengeFetchError("Failed to fetch or parse challenges from CryptoHack") from e

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        """Submit a flag for a challenge."""
        try:
            csrf_token = await get_csrf_token(self._client._http)
            response = await self._client.post(
                f"/api/submit/{challenge_id}.json",
                data={"flag": flag, "_csrf_token": csrf_token},
            )

            if response.status_code == 302:
                raise NotAuthenticatedError()

            data = response.json()
            msg = data.get("message")

            if msg == "Challenge does not exist!":
                raise ChallengeNotFoundError(challenge_id)

            return SubmissionResult(correct=msg == "Success!", message=msg)

        except (NotAuthenticatedError, ChallengeNotFoundError):
            raise
        except Exception as e:
            logger.debug("Error while submitting flag for challenge %s", challenge_id, exc_info=e)
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Failed to submit flag"
            ) from e
