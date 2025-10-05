import logging
from typing import List

from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.exceptions import NotAuthenticatedError, ScoreboardFetchError, NotAuthorizedError
from ctfbridge.models.scoreboard import ScoreboardEntry
from ctfbridge.platforms.htb.http.endpoints import Endpoints
from ctfbridge.platforms.htb.models.scoreboard import HTBScoreboardEntry

logger = logging.getLogger(__name__)


class HTBScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

    async def _fetch_scoreboard(self, limit) -> List[ScoreboardEntry]:
        try:
            response = await self._client.get(
                Endpoints.Scoreboard.get_scoreboard(self._client._ctf_id)
            )

            if response.status_code == 401:
                raise NotAuthenticatedError()
            elif response.status_code == 403:
                raise NotAuthorizedError()

            data = response.json().get("scores", [])
        except (NotAuthenticatedError, NotAuthorizedError):
            raise
        except Exception as e:
            logger.debug("Failed to fetch scoreboard")
            raise ScoreboardFetchError("Invalid response format from server (scoreboard).") from e

        scoreboard = [
            HTBScoreboardEntry(**entry, rank=pos + 1).to_core_model()
            for pos, entry in enumerate(data)
        ]
        return scoreboard
