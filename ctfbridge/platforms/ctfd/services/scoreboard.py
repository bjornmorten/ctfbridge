from typing import List
from urllib.parse import unquote, urlparse

from ctfbridge.exceptions import ScoreboardFetchError
from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.models.scoreboard import ScoreboardEntry

import logging

logger = logging.getLogger(__name__)


class CTFdScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

    async def get_top(self, limit: int = 0) -> List[ScoreboardEntry]:
        resp = await self._client._http.get(
            f"{self._client._platform_url}/api/v1/scoreboard",
        )

        try:
            data = resp.json()["data"]
        except Exception as e:
            raise ScoreboardFetchError(
                "Invalid response format from server (scoreboard)."
            ) from e

        scoreboard = []
        for entry in data:
            scoreboard.append(
                ScoreboardEntry(
                    name=entry.get("name", "unknown"),
                    score=entry.get("score", 0),
                    rank=entry.get("pos", 0),
                )
            )

        if limit:
            return scoreboard[:limit]
        else:
            return scoreboard
