from abc import ABC, abstractmethod
from typing import List

from ctfbridge.models.scoreboard import ScoreboardEntry


class ScoreboardService(ABC):
    """
    Abstract base class for accessing scoreboard data.

    This service defines an interface for retrieving top-ranking teams or users
    from a CTF platform's scoreboard.
    """

    def __init__(self, client):
        """
        Initialize the scoreboard service.

        Args:
            client: A reference to the CTF platform client.
        """
        self.client = client

    @abstractmethod
    def get_top(self, limit: int = 0) -> List[ScoreboardEntry]:
        """
        Return the top scoreboard entries.

        Args:
            limit (int): Maximum number of entries to return. If 0, return all entries.

        Returns:
            List[ScoreboardEntry]: A list of scoreboard entries sorted by rank or score.
        """
        pass

