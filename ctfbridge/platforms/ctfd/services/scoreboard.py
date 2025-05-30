"""CTFd scoreboard service"""

import logging
from typing import List

from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.exceptions import ScoreboardFetchError
from ctfbridge.models.scoreboard import ScoreboardEntry
from ctfbridge.platforms.ctfd.http.endpoints import Endpoints
from ctfbridge.platforms.ctfd.parsers.scoreboard_parser import parse_scoreboard_entry

logger = logging.getLogger(__name__)


class CTFdScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

    async def _fetch_scoreboard(self, limit) -> List[ScoreboardEntry]:
        try:
            resp = await self._client.get(Endpoints.Scoreboard.FULL)
            data = resp.json().get("data", [])
        except Exception as e:
            logger.debug("Failed to fetch scoreboard")
            raise ScoreboardFetchError("Invalid response format from server (scoreboard).") from e

        scoreboard = [parse_scoreboard_entry(entry) for entry in data]
        return scoreboard
