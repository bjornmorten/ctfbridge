import logging
import re
from typing import List, Set

logger = logging.getLogger(__name__)

# Match markdown-style links: [text](http://example.com)
MARKDOWN_LINK_RE = re.compile(r"\[.*?\]\((https?://[^\s)]+)\)", re.IGNORECASE)

# Match bare URLs: http(s)://...
BARE_URL_RE = re.compile(r"\bhttps?://[^\s)\"'<>]+", re.IGNORECASE)

# Match HTML <a href="..."> links
HTML_HREF_RE = re.compile(r'<a\s[^>]*href=["\'](https?://[^"\']+)["\']', re.IGNORECASE)


def extract_links(text: str) -> List[str]:
    """Extract HTTP(S) links from text content.

    Finds links in various formats:
    - Markdown links: [text](http://example.com)
    - Bare URLs: http://example.com
    - HTML links: <a href="http://example.com">

    Args:
        text: The text to extract links from.

    Returns:
        A sorted list of unique URLs found in the text.
    """
    try:
        links: Set[str] = set()

        links.update(MARKDOWN_LINK_RE.findall(text))
        links.update(BARE_URL_RE.findall(text))
        links.update(HTML_HREF_RE.findall(text))

        return sorted(links)
    except Exception as e:
        logger.error(f"Failed to extract links: {e}")
        return []
