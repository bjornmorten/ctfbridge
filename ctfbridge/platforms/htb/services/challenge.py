import logging
from typing import List

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions import SubmissionError
from ctfbridge.exceptions.auth import (
    NotAuthenticatedError,
    NotAuthorizedError,
)
from ctfbridge.exceptions.challenge import ChallengeFetchError, ChallengeNotFoundError
from ctfbridge.models.challenge import Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.platforms.htb.http.endpoints import Endpoints
from ctfbridge.platforms.htb.models.challenge import HTBChallenge, HTBSubmission

logger = logging.getLogger(__name__)


class HTBChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

        # cache challenge categories so we don't have to fetch them every time
        self._category_cache = set()

    @property
    def base_has_details(self) -> bool:
        return True

    async def _fetch_challenges(self) -> List[Challenge]:
        try:
            response = await self._client.get(Endpoints.Ctf.get_details(self._client._ctf_id))
            data = response.json()

            if response.status_code == 401:
                raise NotAuthenticatedError()
            elif response.status_code == 403:
                raise NotAuthorizedError()

            categories = await self._get_challenge_categories()
            challenges = data["challenges"]

            challenges = [
                HTBChallenge(**chal, category=categories.get(chal.get("category_id")))
                for chal in challenges
            ]

            return [challenge.to_core_model() for challenge in challenges]

        except (NotAuthenticatedError, NotAuthorizedError):
            raise
        except Exception as e:
            logger.debug("Error while fetching or parsing challenges", exc_info=e)
            raise ChallengeFetchError("Failed to fetch or parse challenges from HTB") from e

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        try:
            response = await self._client.post(
                Endpoints.Challenges.SUBMIT_FLAG,
                json={"challenge_id": challenge_id, "flag": flag},
            )

            if response.status_code == 401:
                raise NotAuthenticatedError()
            elif response.status_code == 403:
                raise NotAuthorizedError()
            elif response.status_code == 302:
                raise ChallengeNotFoundError(challenge_id)

            message = response.json().get("message")

            if response.status_code == 200:
                correct = True
            elif response.status_code == 400:
                correct = False
            else:
                correct = False

            submission = HTBSubmission(correct=correct, message=message)
            return submission.to_core_model()

        except (NotAuthenticatedError, NotAuthorizedError, ChallengeNotFoundError):
            raise
        except Exception as e:
            logger.debug("Error while submitting flag for challenge %s", challenge_id, exc_info=e)
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Failed to submit flag"
            ) from e

    async def _get_challenge_categories(self) -> dict[int, str]:
        if not self._category_cache:
            resp = await self._client.get(Endpoints.Challenges.CATEGORIES)
            self._category_cache = {item["id"]: item["name"] for item in resp.json()}
        return self._category_cache
