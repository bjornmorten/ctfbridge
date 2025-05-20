import logging
from typing import List

from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.exceptions import ScoreboardFetchError
from ctfbridge.models.scoreboard import ScoreboardEntry

logger = logging.getLogger(__name__)


class HTBScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

    async def get_top(self, limit: int = 0) -> List[ScoreboardEntry]:
        resp = await self._client._http.get(
            self._client._get_api_url(f"ctfs/scores/{self._client._ctf_id}")
        )

        try:
            data = resp.json()["scores"]
        except Exception as e:
            raise ScoreboardFetchError(
                "Invalid response format from server (scoreboard)."
            ) from e

        scoreboard = []
        for i, entry in enumerate(data):
            scoreboard.append(
                ScoreboardEntry(
                    name=entry.get("name"),
                    score=entry.get("points", 0),
                    rank=i + 1,
                )
            )

        if limit:
            return scoreboard[:limit]
        else:
            return scoreboard
