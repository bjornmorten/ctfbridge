from abc import ABC, abstractmethod
from typing import List

from ctfbridge.models.scoreboard import ScoreboardEntry


class ScoreboardService(ABC):
    """
    Class for accessing scoreboard data.
    """

    async def get_top(self, limit: int = 0) -> List[ScoreboardEntry]:
        """
        Return the top scoreboard entries.

        Args:
            limit (int): Maximum number of entries to return. If 0, return all entries.

        Returns:
            List[ScoreboardEntry]: A list of scoreboard entries sorted by rank or score.
        """
        raise NotImplementedError
