import logging
from typing import List, Optional, Type

from ctfbridge.models.challenge import Challenge
from ctfbridge.processors.base import BaseChallengeParser
from ctfbridge.processors.registry import get_all_parsers

logger = logging.getLogger(__name__)


class ChallengeEnricher:
    """Enriches challenge objects by applying registered parsers."""

    def __init__(self, parser_classes: Optional[List[Type[BaseChallengeParser]]] = None):
        """Initialize the enricher.

        Args:
            parser_classes: Optional list of specific parser classes to use.
                          If None, all registered parsers will be used.
        """
        self.parsers = []
        if parser_classes:
            self.parsers = [cls() for cls in parser_classes]
        else:
            self.parsers = get_all_parsers()

        logger.debug(f"Initialized enricher with {len(self.parsers)} parsers")

    def parse(self, challenge: Challenge, raise_errors: bool = False) -> Challenge:
        """Parse and enrich a challenge object.

        Args:
            challenge: The challenge to enrich.
            raise_errors: If True, raises exceptions from parsers.
                        If False, logs errors and continues.

        Returns:
            The enriched challenge object.

        Raises:
            ValueError: If the challenge is None.
            Exception: Any exception from parsers if raise_errors is True.
        """
        if challenge is None:
            raise ValueError("Cannot enrich None challenge")

        for parser in self.parsers:
            try:
                challenge = parser.apply(challenge)
            except Exception as e:
                error_msg = f"Parser {parser.name} failed on challenge {challenge.id}: {str(e)}"
                if raise_errors:
                    raise
                else:
                    logger.error(error_msg)

        return challenge


# Global enricher instance with default configuration
enricher = ChallengeEnricher()


def enrich_challenge(challenge: Challenge, raise_errors: bool = False) -> Challenge:
    """Convenience function to enrich a challenge using the global enricher.

    Args:
        challenge: The challenge to enrich.
        raise_errors: Whether to raise parser errors.

    Returns:
        The enriched challenge.
    """
    return enricher.parse(challenge, raise_errors=raise_errors)
