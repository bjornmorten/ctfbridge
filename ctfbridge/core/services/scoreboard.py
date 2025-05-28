from abc import abstractmethod
from typing import List

from ctfbridge.base.services.scoreboard import ScoreboardService
from ctfbridge.models.scoreboard import ScoreboardEntry


class CoreScoreboardService(ScoreboardService):
    def __init__(self, client):
        self._client = client

    async def get_top(self, limit: int = 0) -> List[ScoreboardEntry]:
        scoreboard = await self._fetch_scoreboard(limit)

        return scoreboard if limit == 0 else scoreboard[:limit]

    @abstractmethod
    async def _fetch_scoreboard(self, limit) -> List[ScoreboardEntry]:
        pass
