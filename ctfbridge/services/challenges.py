from abc import ABC, abstractmethod
from typing import List, Optional

from ctfbridge.models.challenge import Challenge
from ctfbridge.utils.normalization import normalize_category


class ChallengeService(ABC):
    """
    Abstract base class for challenge-related operations.

    This service provides a standard interface for fetching and submitting
    challenges, as well as utility methods to filter challenges by category
    or name.
    """


    def __init__(self, client):
        """
        Initialize the challenge service.

        Args:
            client: A reference to the platform client, used to perform API requests.
        """
        self.client = client

    @abstractmethod
    def get_all(self) -> List[Challenge]:
        """
        Fetch all challenges from the platform.

        Returns:
            List[Challenge]: A list of all available challenges.
        """
        pass

    @abstractmethod
    def get_by_id(self, challenge_id: int) -> Challenge:
        """
        Fetch a single challenge by its ID.

        Args:
            challenge_id (int): The ID of the challenge to retrieve.

        Returns:
            Challenge: The corresponding challenge object.
        """
        pass

    @abstractmethod
    def submit(self, challenge_id: int, flag: str):
        """
        Submit a flag for a given challenge.

        Args:
            challenge_id (int): The ID of the challenge to submit the flag for.
            flag (str): The flag string to submit.
        """
        pass

    def filter_by_category(self, category: str) -> List[Challenge]:
        """
        Filter challenges by category (normalized).

        Args:
            category (str): The category to filter by.

        Returns:
            List[Challenge]: A list of challenges matching the given category.
        """
        norm = normalize_category(category)
        return [c for c in self.get_all() if normalize_category(c.category) == norm]

    def filter_by_name(self, name: str) -> List[Challenge]:
        """
        Filter challenges whose name includes the given text (case-insensitive).

        Args:
            name (str): Substring to search for in the challenge names.

        Returns:
            List[Challenge]: A list of matching challenges.
        """
        return [c for c in self.get_all() if name.lower() in c.name.lower()]

