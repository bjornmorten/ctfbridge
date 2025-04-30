from abc import ABC, abstractmethod
from typing import List

from ctfbridge.models.scoreboard import ScoreboardEntry


class ScoreboardService(ABC):
    """
    Base scoreboard service.
    """

    def __init__(self, client):
        self.client = client

    @abstractmethod
    def get_top(self, limit: int = 0) -> List[ScoreboardEntry]:
        """
        Return the top scoreboard entries.

        Args:
            limit: Optional limit of how many entries to return. 0 = all.
        """
        pass

