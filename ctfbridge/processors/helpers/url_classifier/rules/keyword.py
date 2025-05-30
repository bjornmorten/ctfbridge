import re
from typing import Tuple

from ..utils import LinkClassifierContext

# Keywords that suggest service endpoints
SERVICE_KEYWORDS: Tuple[str, ...] = ("run", "host", "port", "listen", "api", "docker", "service")

# Keywords that suggest downloadable content
ATTACHMENT_KEYWORDS: Tuple[str, ...] = ("file", "download", "resource", "attachment", "artifact")


def _has_word(text: str, word: str) -> bool:
    """Check if a word exists with word boundaries.

    This prevents partial matches like 'data' matching 'database'.

    Args:
        text: The text to search in.
        word: The word to search for.

    Returns:
        True if the word is found with word boundaries.
    """
    pattern = rf"\b{re.escape(word)}\b"
    return bool(re.search(pattern, text))


def is_likely_service(ctx: LinkClassifierContext) -> bool:
    """Check if the URL contains service-related keywords.

    Looks for service-related keywords in both the path and hostname.

    Args:
        ctx: The URL classification context.

    Returns:
        True if service-related keywords are found.
    """
    path = ctx.parsed.path.lower()
    netloc = ctx.parsed.netloc.lower()
    return any(_has_word(path, kw) or _has_word(netloc, kw) for kw in SERVICE_KEYWORDS)


def is_likely_attachment(ctx: LinkClassifierContext) -> bool:
    """Check if the URL contains attachment-related keywords.

    Looks for attachment-related keywords in both the path and hostname.

    Args:
        ctx: The URL classification context.

    Returns:
        True if attachment-related keywords are found.
    """
    path = ctx.parsed.path.lower()
    netloc = ctx.parsed.netloc.lower()
    return any(_has_word(path, kw) or _has_word(netloc, kw) for kw in ATTACHMENT_KEYWORDS)
