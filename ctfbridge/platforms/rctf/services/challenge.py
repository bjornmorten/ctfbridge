import logging
from typing import List

import httpx

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions import (
    ChallengeFetchError,
    SubmissionError,
    NotAuthenticatedError,
    ChallengesUnavailableError,
)  # Added NotAuthenticatedError
from ctfbridge.models.challenge import Challenge as CoreChallenge
from ctfbridge.models.submission import SubmissionResult as CoreSubmissionResult

# Import new rCTF specific models and endpoints
from ctfbridge.platforms.rctf.models.challenge import (
    RCTFChallengeData,
    RCTFSubmissionResponse,
)
from ctfbridge.platforms.rctf.models.user import (
    RCTFUserProfileData,
)
from ctfbridge.platforms.rctf.http.endpoints import Endpoints

logger = logging.getLogger(__name__)


class RCTFChallengeService(CoreChallengeService):
    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return True

    async def _fetch_profile(self) -> RCTFUserProfileData:
        """
        Fetches the current user's profile from rCTF, primarily to get solved challenges.
        """
        try:
            response = await self._client.get(Endpoints.Users.ME)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json().get("data", {})
            return RCTFUserProfileData(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:  # Unauthorized
                logger.warning(f"Unauthorized when fetching rCTF profile: {e}")
                raise NotAuthenticatedError(
                    "Authentication required to fetch rCTF user profile."
                ) from e
            logger.error(f"HTTP error fetching rCTF profile: {e}")
            raise ChallengeFetchError(
                f"Failed to fetch rCTF user profile: {e.response.status_code}"
            ) from e
        except (
            ValueError,
            TypeError,
        ) as e:  # Handles JSON decoding errors or Pydantic validation errors
            logger.error(f"Error parsing rCTF profile data: {e}")
            raise ChallengeFetchError(
                "Invalid response format from rCTF server (user profile)."
            ) from e

    async def _fetch_challenges(self) -> List[CoreChallenge]:
        try:
            response = await self._client.get(Endpoints.Challenges.LIST)
            response.raise_for_status()  # Check for HTTP errors
            raw_challs_data = response.json().get("data", [])
            if not isinstance(raw_challs_data, list):
                logger.error(f"Unexpected format for challenges data from rCTF: {raw_challs_data}")
                raise ChallengeFetchError("Invalid challenges data format from rCTF.")

            # Fetch profile to determine solved status
            # This might fail if not authenticated, but some CTFs might allow viewing challenges without auth
            profile = None
            solved_ids = set()
            try:
                profile = await self._fetch_profile()
                solved_ids = {solve.id for solve in profile.solves}
            except NotAuthenticatedError:
                logger.info(
                    "Could not fetch rCTF profile for solved status (likely not authenticated). Proceeding without it."
                )
            except ChallengeFetchError as e:  # Catch errors from _fetch_profile specifically
                logger.warning(
                    f"Could not fetch rCTF profile for solved status due to: {e}. Proceeding without it."
                )

            challenges: List[CoreChallenge] = []
            for chall_data in raw_challs_data:
                if not isinstance(chall_data, dict):
                    logger.warning(f"Skipping invalid challenge data item: {chall_data}")
                    continue
                try:
                    rctf_chal = RCTFChallengeData(**chall_data)
                    solved_status = rctf_chal.id in solved_ids
                    challenges.append(rctf_chal.to_core_model(solved=solved_status))
                except Exception as e:  # Catch Pydantic validation error for individual challenge
                    logger.error(
                        f"Failed to parse individual rCTF challenge data ('{chall_data.get('name', 'N/A')}'): {e}"
                    )
                    # Optionally, skip this challenge and continue
            return challenges
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.warning(f"Unauthorized when fetching rCTF challenges: {e}")
                raise NotAuthenticatedError(
                    "Authentication may be required to fetch rCTF challenges."
                ) from e
            logger.error(f"HTTP error fetching rCTF challenges: {e}")
            raise ChallengeFetchError(
                f"Failed to fetch challenges from rCTF: {e.response.status_code}"
            ) from e
        except (
            ValueError,
            TypeError,
        ) as e:  # Handles JSON decoding errors or top-level Pydantic validation errors
            logger.error(f"Error parsing rCTF challenges data: {e}")
            raise ChallengeFetchError(
                "Invalid response format from rCTF server (challenges)."
            ) from e

    async def submit(self, challenge_id: str, flag: str) -> CoreSubmissionResult:
        url = Endpoints.Challenges.submit(challenge_id=challenge_id)
        payload = {"flag": flag}

        try:
            response = await self._client.post(url, json=payload)
            # rCTF often returns 200 OK even for bad flags, relies on 'kind' field
            # However, it might return other statuses for issues like challenge not found, CTF ended, etc.
            # For example, 400 for "Flag is empty", 403 if not started/ended, 404 if chall id is wrong type
            # 401 if not logged in.

            if response.status_code == 401:
                if "badEnded" in response.text or "badNotStarted" in response.text:
                    raise ChallengesUnavailableError
                raise NotAuthenticatedError("Authentication required to submit flags to rCTF.")

            # For other non-200 statuses that aren't auth related, treat as submission failure
            if response.status_code != 200:
                error_message = f"Submission failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    error_message = error_data.get("message", error_message)
                except ValueError:  # Not JSON
                    pass
                raise SubmissionError(challenge_id=challenge_id, flag=flag, reason=error_message)

            submission_data = response.json()
            rctf_submission = RCTFSubmissionResponse(**submission_data)
            return rctf_submission.to_core_model()
        except httpx.HTTPStatusError as e:  # Should be caught by the check above, but as a fallback
            error_message = f"Submission failed with status {e.response.status_code}"
            try:
                error_data = e.response.json()
                error_message = error_data.get("message", error_message)
            except ValueError:
                pass
            logger.error(f"HTTP error submitting flag to rCTF: {e}")
            raise SubmissionError(challenge_id=challenge_id, flag=flag, reason=error_message) from e
        except (
            ValueError,
            TypeError,
        ) as e:  # Handles JSON decoding errors or Pydantic validation errors
            logger.error(f"Error parsing rCTF submission response: {e}")
            raise SubmissionError(
                challenge_id=challenge_id,
                flag=flag,
                reason="Invalid response format from rCTF server (submission).",
            ) from e
        except NotAuthenticatedError:  # Re-raise
            raise
        except Exception as e:  # Catch any other unexpected errors
            logger.exception(
                f"Unexpected error during rCTF flag submission for challenge {challenge_id}"
            )
            raise SubmissionError(
                challenge_id=challenge_id,
                flag=flag,
                reason=f"An unexpected error occurred: {str(e)}",
            )
