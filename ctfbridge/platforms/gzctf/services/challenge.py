import logging
from typing import List

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions import SubmissionError
from ctfbridge.exceptions.auth import NotAuthenticatedError
from ctfbridge.exceptions.challenge import ChallengeFetchError
from ctfbridge.models.challenge import Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.platforms.gzctf.http.endpoints import Endpoints
from ctfbridge.platforms.gzctf.models.challenge import GZCTFChallenge, GZCTFSubmission

logger = logging.getLogger(__name__)


class GZCTFChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

        # cache solved challenge IDs so we don't have to fetch them every time
        # we do a lookup on a single, but it's a problem if it's a long time
        # since we did a lookup for all challenges where the state also is
        self._solved_challenge_ids = set()

    @property
    def base_has_details(self) -> bool:
        return False

    async def _fetch_challenges(self) -> List[Challenge]:
        try:
            response = await self._client.get(Endpoints.Ctf.get_details(self._client._ctf_id))
            data = response.json()

            if response.status_code == 401:
                raise NotAuthenticatedError()

            categories = data.get("challenges")
            challenges = [chal for category in categories.values() for chal in category]

            self._solved_challenge_ids = {
                solved_chal.get("id") for solved_chal in data.get("rank").get("solvedChallenges")
            }

            challenges = [
                GZCTFChallenge(**chal, is_solved=chal.get("id") in self._solved_challenge_ids)
                for chal in challenges
            ]

            return [challenge.to_core_model() for challenge in challenges]

        except Exception as e:
            logger.debug("Error while fetching or parsing challenges", exc_info=e)
            raise ChallengeFetchError("Failed to fetch or parse challenges from GZCTF") from e

    async def _fetch_challenge_by_id(self, challenge_id: str) -> Challenge:
        try:
            url = Endpoints.Challenges.detail(ctf_id=self._client._ctf_id, id=challenge_id)
            response = await self._client.get(url)
            chal = response.json()
            # TODO: make better solution?
            # The is_solved may be wrong if we didn't refresh all challenges since a solve.
            challenge = GZCTFChallenge(
                **chal, is_solved=chal.get("id") in self._solved_challenge_ids
            )
            return challenge.to_core_model()
        except Exception as e:
            logger.debug("Error while fetching or parsing challenge %s", challenge_id, exc_info=e)
            raise ChallengeFetchError(
                f"Failed to fetch or parse challenge {challenge_id} from CTFd"
            ) from e

    async def submit(self, challenge_id: str, flag: str) -> SubmissionResult:
        try:
            response = await self._client.post(
                Endpoints.Challenges.submit_flag(self._client._ctf_id, id=challenge_id),
                json={"flag": flag},
            )

            if response.status_code == 401:
                raise NotAuthenticatedError()

            submission_id = response.json()

            response = await self._client.get(
                Endpoints.Challenges.get_flag_submission_result(
                    self._client._ctf_id, id=challenge_id, submission_id=submission_id
                ),
            )

            result = response.json()

            if result == "Accepted":
                correct = True
            elif result == "WrongAnswer":
                correct = False
            else:
                correct = False

            submission = GZCTFSubmission(correct=correct, message=result)
            return submission.to_core_model()

        except Exception as e:
            logger.debug("Error while submitting flag for challenge %s", challenge_id, exc_info=e)
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason="Failed to submit flag"
            ) from e
