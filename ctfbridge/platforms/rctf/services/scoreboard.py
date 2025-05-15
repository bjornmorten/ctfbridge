from typing import List

from ctfbridge.exceptions import ScoreboardFetchError
from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.models.scoreboard import ScoreboardEntry

import logging

logger = logging.getLogger(__name__)


class RCTFScoreboardService(CoreScoreboardService):
    def __init__(self, client):
        self._client = client

    async def get_top(self, limit: int = 0) -> List[ScoreboardEntry]:
        resp = await self._client._http.get(
            f"{self._client._platform_url}/api/v1/leaderboard/now?limit=0&offset=100"
        )

        try:
            total = resp.json()["data"]["total"]
        except Exception as e:
            raise ScoreboardFetchError(
                "Invalid response format from server (scoreboard)."
            ) from e

        if limit:
            limit = min(limit, total)
        else:
            limit = total

        scoreboard = []
        for offset in range(0, limit, 100):
            curr_limit = min(100, limit - offset)
            resp = await self._client._http.get(
                f"{self._client._platform_url}/api/v1/leaderboard/now?limit={curr_limit}&offset={offset}"
            )

            partial_scoreboard = resp.json()["data"]["leaderboard"]
            for i, entry in enumerate(partial_scoreboard):
                scoreboard.append(
                    ScoreboardEntry(
                        name=entry["name"], score=entry["score"], rank=offset + i + 1
                    )
                )

        return scoreboard
