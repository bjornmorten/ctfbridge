from dataclasses import dataclass
from urllib.parse import ParseResult


@dataclass
class LinkClassifierContext:
    """Context object for URL classification rules.

    This class holds both the original URL string and its parsed components
    to avoid repeated parsing in classification rules.

    Attributes:
        link: The original URL string.
        parsed: The parsed URL components.
    """

    link: str
    parsed: ParseResult
