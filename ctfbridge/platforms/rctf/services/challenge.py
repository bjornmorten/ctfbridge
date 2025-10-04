import logging
from typing import List

import httpx

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions import (
    ChallengeFetchError,
    ChallengesUnavailableError,
    NotAuthenticatedError,
    SubmissionError,
)
from ctfbridge.models.challenge import Challenge as CoreChallenge
from ctfbridge.models.submission import SubmissionResult as CoreSubmissionResult
from ctfbridge.platforms.rctf.http.endpoints import Endpoints
from ctfbridge.platforms.rctf.models.challenge import RCTFChallengeData
from ctfbridge.platforms.rctf.models.submission import RCTFSubmissionResponse
from ctfbridge.platforms.rctf.models.user import RCTFUserProfileData

logger = logging.getLogger(__name__)


class RCTFChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return True

    async def _fetch_profile(self) -> RCTFUserProfileData:
        """
        Fetch user profile to determine solved challenges.
        """
        try:
            response = await self._client.get(Endpoints.Users.ME)
            response.raise_for_status()
            data = response.json().get("data", {})
            return RCTFUserProfileData(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.warning("Unauthorized when fetching rCTF profile.")
                raise NotAuthenticatedError(
                    "Authentication required to fetch rCTF user profile."
                ) from e
            logger.error(f"HTTP error fetching rCTF profile: {e}")
            raise ChallengeFetchError(
                f"Failed to fetch rCTF user profile: {e.response.status_code}"
            ) from e
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing rCTF profile data: {e}")
            raise ChallengeFetchError(
                "Invalid response format from rCTF server (user profile)."
            ) from e

    async def _get_solved_ids(self) -> set[str]:
        """
        Safely retrieve a set of solved challenge IDs.
        """
        profile = await self._fetch_profile()
        return {solve.id for solve in profile.solves}

    async def _fetch_challenges(self) -> List[CoreChallenge]:
        """
        Fetch all available rCTF challenges.
        """
        try:
            response = await self._client.get(Endpoints.Challenges.LIST)
            response.raise_for_status()

            raw_data = response.json().get("data", [])
            if not isinstance(raw_data, list):
                logger.error(f"Unexpected challenge data format: {raw_data}")
                raise ChallengeFetchError("Invalid challenges data format from rCTF.")

            solved_ids = await self._get_solved_ids()
            challenges: List[CoreChallenge] = []

            for item in raw_data:
                if not isinstance(item, dict):
                    logger.warning(f"Skipping invalid challenge entry: {item}")
                    continue
                try:
                    rctf_chal = RCTFChallengeData(**item)
                    challenges.append(rctf_chal.to_core_model(solved=rctf_chal.id in solved_ids))
                except Exception as e:
                    logger.error(f"Failed to parse challenge '{item.get('name', 'unknown')}': {e}")

            return challenges

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.warning("Unauthorized when fetching rCTF challenges.")
                raise NotAuthenticatedError(
                    "Authentication may be required to fetch rCTF challenges."
                ) from e
            logger.error(f"HTTP error fetching rCTF challenges: {e}")
            raise ChallengeFetchError(
                f"Failed to fetch challenges from rCTF: {e.response.status_code}"
            ) from e
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing rCTF challenges: {e}")
            raise ChallengeFetchError(
                "Invalid response format from rCTF server (challenges)."
            ) from e

    async def submit(self, challenge_id: str, flag: str) -> CoreSubmissionResult:
        """
        Submit a flag for a challenge.
        """
        url = Endpoints.Challenges.submit(challenge_id=challenge_id)
        payload = {"flag": flag}

        try:
            response = await self._client.post(url, json=payload)

            if response.status_code == 401:
                if "badEnded" in response.text or "badNotStarted" in response.text:
                    raise ChallengesUnavailableError
                raise NotAuthenticatedError("Authentication required to submit flags.")

            if response.status_code not in [200, 400, 409]:
                try:
                    error = response.json().get("message", f"HTTP {response.status_code}")
                except Exception:
                    error = f"HTTP {response.status_code}"
                raise SubmissionError(challenge_id=challenge_id, flag=flag, reason=error)

            data = response.json()
            submission = RCTFSubmissionResponse(**data)
            return submission.to_core_model()

        except NotAuthenticatedError:
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during flag submission: {e}")
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason=f"HTTP error {e.response.status_code}"
            ) from e
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing submission response: {e}")
            raise SubmissionError(
                challenge_id=challenge_id,
                flag=flag,
                reason="Invalid response format from rCTF server (submission).",
            ) from e
        except Exception as e:
            logger.exception(f"Unexpected error submitting flag to challenge {challenge_id}")
            raise SubmissionError(
                challenge_id=challenge_id, flag=flag, reason=f"Unexpected error: {str(e)}"
            )
