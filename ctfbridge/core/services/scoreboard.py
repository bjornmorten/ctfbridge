from abc import abstractmethod
from typing import List

from ctfbridge.base.services.scoreboard import ScoreboardService
from ctfbridge.models.scoreboard import ScoreboardEntry


class CoreScoreboardService(ScoreboardService):
    """
    Core implementation of the scoreboard service.
    Provides common scoreboard fetching and filtering functionality.
    """

    def __init__(self, client):
        """
        Initialize the scoreboard service.

        Args:
            client: The CTF client instance
        """
        self._client = client

    async def get_top(self, limit: int = 0) -> List[ScoreboardEntry]:
        scoreboard = await self._fetch_scoreboard(limit)

        return scoreboard if limit == 0 else scoreboard[:limit]

    async def _fetch_scoreboard(self, limit) -> List[ScoreboardEntry]:
        """
        Fetch the scoreboard from the platform.
        Must be implemented by platform-specific services.

        Args:
            limit: Maximum number of entries to fetch (0 for all)

        Returns:
            List of scoreboard entries
        """
        pass
