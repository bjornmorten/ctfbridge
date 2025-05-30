from abc import ABC, abstractmethod
from typing import Optional

from ctfbridge.models.challenge import Challenge


class BaseChallengeParser(ABC):
    """Base class for all challenge parsers.

    Challenge parsers are responsible for extracting and enriching information
    from challenge objects. Each parser should focus on a specific aspect of
    the challenge data.
    """

    @property
    def name(self) -> str:
        """Return the name of the parser for logging and debugging."""
        return self.__class__.__name__

    def can_handle(self, challenge: Challenge) -> bool:
        """Check if this parser should process the challenge.

        Args:
            challenge: The challenge to check.

        Returns:
            True if this parser can handle the challenge, False otherwise.
        """
        return True

    @abstractmethod
    def _process(self, challenge: Challenge) -> Challenge:
        """Internal method to process a challenge.

        This method should be implemented by subclasses to do the actual
        processing work.

        Args:
            challenge: The challenge to process.

        Returns:
            The processed challenge.
        """
        pass

    def apply(self, challenge: Challenge) -> Challenge:
        """Apply the parser to a challenge object.

        Args:
            challenge: The challenge to process.

        Returns:
            The processed challenge.
        """
        if not self.can_handle(challenge):
            return challenge

        return self._process(challenge)
