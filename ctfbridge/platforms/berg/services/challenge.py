"""Berg challenge service implementation"""

import logging
from typing import List

from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.exceptions.challenge import ChallengeFetchError
from ctfbridge.models.challenge import Challenge
from ctfbridge.platforms.berg.http.endpoints import Endpoints
from ctfbridge.platforms.berg.models.challenge import BergChallenge

logger = logging.getLogger(__name__)


class BergChallengeService(CoreChallengeService):
    """Service for interacting with Berg challenge endpoints"""

    def __init__(self, client):
        self._client = client

    @property
    def base_has_details(self) -> bool:
        return True

    async def _fetch_challenges(self) -> List[Challenge]:
        """Fetch list of all challenges."""
        try:
            response = await self._client.get(Endpoints.Challenges.LIST)

            data = response.json()
            challenges = [BergChallenge(**chal) for chal in data]
            return [challenge.to_core_model() for challenge in challenges]

        except Exception as e:
            logger.debug("Error while fetching or parsing challenges", exc_info=e)
            raise ChallengeFetchError("Failed to fetch or parse challenges from Berg") from e
