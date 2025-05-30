import re

from ..utils import LinkClassifierContext

# Match port numbers in URLs (either in hostname:port or ?port=number format)
PORT_PATTERN = re.compile(r"(?::|port=)(\d{2,5})")


def has_explicit_port(ctx: LinkClassifierContext) -> bool:
    """Check if the URL has an explicit port number.

    Looks for port numbers in two formats:
    - Standard URL port (hostname:port)
    - Query parameter (?port=number)

    Args:
        ctx: The URL classification context.

    Returns:
        True if an explicit port number is found.
    """
    return bool(ctx.parsed.port or PORT_PATTERN.search(ctx.link))
