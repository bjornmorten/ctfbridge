from abc import ABC, abstractmethod
from typing import List, Optional

from ctfbridge.models.challenge import Challenge
from ctfbridge.utils.normalization import normalize_category


class ChallengeService(ABC):
    """
    Base challenge service. Provides filtering logic; platforms override fetch/submit.
    """

    def __init__(self, client):
        self.client = client

    @abstractmethod
    def get_all(self) -> List[Challenge]:
        """Fetch all challenges from the platform."""
        pass

    @abstractmethod
    def get_by_id(self, challenge_id: int) -> Challenge:
        """Fetch a specific challenge by ID."""
        pass

    @abstractmethod
    def submit(self, challenge_id: int, flag: str):
        """Submit a flag for a challenge."""
        pass

    def filter_by_category(self, category: str) -> List[Challenge]:
        """
        Return challenges whose category matches the normalized category.
        """
        norm = normalize_category(category)
        return [c for c in self.get_all() if normalize_category(c.category) == norm]

    def filter_by_name(self, name: str) -> List[Challenge]:
        """
        Return challenges whose name includes the given text (case-insensitive).
        """
        return [c for c in self.get_all() if name.lower() in c.name.lower()]

