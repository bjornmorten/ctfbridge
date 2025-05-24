import logging
from typing import List

from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.exceptions import ScoreboardFetchError
from ctfbridge.models.scoreboard import ScoreboardEntry

logger = logging.getLogger(__name__)


class CTFdScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

    async def get_top(self, limit: int = 0) -> List[ScoreboardEntry]:
        try:
            resp = await self._client.get("scoreboard")
            data = resp.json().get("data", [])
        except Exception as e:
            logger.exception("Failed to fetch scoreboard")
            raise ScoreboardFetchError("Invalid response format from server (scoreboard).") from e

        scoreboard = [
            ScoreboardEntry(
                name=entry.get("name"),
                score=entry.get("score"),
                rank=entry.get("pos"),
            )
            for entry in data
        ]

        return scoreboard[:limit] if limit else scoreboard
