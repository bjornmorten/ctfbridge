import logging
from typing import List

from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.exceptions import NotAuthenticatedError, ScoreboardFetchError
from ctfbridge.models.scoreboard import ScoreboardEntry
from ctfbridge.platforms.gzctf.http.endpoints import Endpoints
from ctfbridge.platforms.gzctf.models.scoreboard import GZCTFScoreboardEntry

logger = logging.getLogger(__name__)


class GZCTFScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

    async def _fetch_scoreboard(self, limit) -> List[ScoreboardEntry]:
        try:
            response = await self._client.get(
                Endpoints.Scoreboard.get_scoreboard(self._client._ctf_id)
            )

            if response.status_code == 401:
                raise NotAuthenticatedError()

            data = response.json().get("items", [])
        except NotAuthenticatedError:
            raise
        except Exception as e:
            logger.debug("Failed to fetch scoreboard")
            raise ScoreboardFetchError("Invalid response format from server (scoreboard).") from e

        scoreboard = [GZCTFScoreboardEntry(**entry).to_core_model() for entry in data]
        return scoreboard
