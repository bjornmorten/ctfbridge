import logging
import re
from typing import List

from ctfbridge.models.challenge import Challenge
from ctfbridge.processors.base import BaseChallengeParser
from ctfbridge.processors.registry import register_parser

logger = logging.getLogger(__name__)

# Match author patterns in description
AUTHOR_PATTERNS = [
    # Multiple authors with commas or 'and'
    r"(?i)authors\s*[:\-]\s*([a-zA-Z0-9_.+-]+(?:[-.][a-zA-Z0-9_.+-]+)*(?:\s*(?:,|\band\b)\s*[a-zA-Z0-9_.+-]+(?:[-.][a-zA-Z0-9_.+-]+)*)*)",
    # Standard author field
    r"(?i)author\s*[:\-]\s*([a-zA-Z0-9_.+-]+(?:[-.][a-zA-Z0-9_.+-]+)*)",
    # Created by format
    r"(?i)created\s+by\s+([a-zA-Z0-9_.+-]+(?:[-.][a-zA-Z0-9_.+-]+)*)",
    # Written by format
    r"(?i)written\s+by\s+([a-zA-Z0-9_.+-]+(?:[-.][a-zA-Z0-9_.+-]+)*)",
    # Made by format
    r"(?i)made\s+by\s+([a-zA-Z0-9_.+-]+(?:[-.][a-zA-Z0-9_.+-]+)*)",
    # Credit format
    r"(?i)credits?\s*[:\-]\s*([a-zA-Z0-9_.+-]+(?:[-.][a-zA-Z0-9_.+-]+)*)",
]

# Compile all patterns
AUTHOR_RES = [re.compile(pattern) for pattern in AUTHOR_PATTERNS]


@register_parser
class AuthorExtractor(BaseChallengeParser):
    """Extracts author information from challenge descriptions."""

    def can_handle(self, challenge: Challenge) -> bool:
        """Check if this parser should process the challenge.

        Returns False if the challenge already has authors or no description.
        """
        return not challenge.authors and bool(challenge.description)

    def _process(self, challenge: Challenge) -> Challenge:
        """Extract author information from the challenge description.

        Tries multiple patterns to find author information, including:
        - Multiple authors separated by commas or 'and'
        - Standard author field
        - Created/written/made by formats
        - Credits attribution

        Args:
            challenge: The challenge to process.

        Returns:
            The challenge with extracted author information.
        """
        if not self.can_handle(challenge):
            return challenge

        try:
            authors = set()  # Use set to avoid duplicates

            # Try each pattern in order
            for pattern in AUTHOR_RES:
                if match := pattern.search(challenge.description):
                    raw_authors = match.group(1).strip()

                    # Split multiple authors if found
                    if "," in raw_authors or " and " in raw_authors:
                        parts = raw_authors.replace(" and ", ",").split(",")
                        for part in parts:
                            author = part.strip()
                            if len(author) > 2:  # Avoid single-char matches
                                authors.add(author)
                    else:
                        author = raw_authors
                        if len(author) > 2:  # Avoid single-char matches
                            authors.add(author)

                    # If we found any authors, stop searching
                    if authors:
                        break

            # Update challenge with found authors
            if authors:
                challenge.authors = sorted(authors)  # Sort for consistent order

        except Exception as e:
            logger.error(f"Failed to extract authors: {e}")

        return challenge
