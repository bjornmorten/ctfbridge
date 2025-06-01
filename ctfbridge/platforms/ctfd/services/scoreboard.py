"""CTFd scoreboard service"""

import logging
from typing import List

from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.exceptions import NotAuthenticatedError, ScoreboardFetchError
from ctfbridge.models.scoreboard import ScoreboardEntry
from ctfbridge.platforms.ctfd.http.endpoints import Endpoints
from ctfbridge.platforms.ctfd.models.scoreboard import CTFdScoreboardEntry

logger = logging.getLogger(__name__)


class CTFdScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

    async def _fetch_scoreboard(self, limit) -> List[ScoreboardEntry]:
        try:
            resp = await self._client.get(Endpoints.Scoreboard.FULL)
            if resp.status_code == 401 or (
                resp.status_code == 302 and "login" in resp.headers.get("location", "")
            ):
                raise NotAuthenticatedError()

            if resp.status_code == 403:
                raise ScoreboardFetchError("Scoreboard is not available")

            data = resp.json().get("data", [])
        except (NotAuthenticatedError, ScoreboardFetchError):
            raise
        except Exception as e:
            logger.debug("Failed to fetch scoreboard")
            raise ScoreboardFetchError("Invalid response format from server (scoreboard).") from e

        scoreboard = [CTFdScoreboardEntry(**entry).to_core_model() for entry in data]
        return scoreboard
