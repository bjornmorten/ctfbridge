import logging
from dataclasses import dataclass
from typing import Dict, List
from urllib.parse import urlparse

from .rules.file_extensions import is_filetype
from .rules.hostname import is_service_hostname, is_storage_hostname
from .rules.keyword import is_likely_attachment, is_likely_service
from .rules.path import is_attachment_path, is_root_path, is_service_path
from .rules.port import has_explicit_port
from .utils import LinkClassifierContext

logger = logging.getLogger(__name__)


@dataclass
class ClassificationResult:
    """Result of URL classification."""

    is_service: bool


def classify_url(link: str) -> ClassificationResult:
    """Classify a single URL as either a service endpoint or attachment.

    Args:
        link: The URL to classify.

    Returns:
        Classification result indicating if URL is a service.

    Raises:
        ValueError: If the URL is invalid or not HTTP(S).
    """
    parsed = urlparse(link)
    if not parsed.scheme.startswith("http"):
        raise ValueError(f"Not an HTTP(S) URL: {link}")

    ctx = LinkClassifierContext(link=link, parsed=parsed)

    # First check for storage services since they're unambiguous
    if is_storage_hostname(ctx):
        return ClassificationResult(is_service=False)

    # Then check service signals
    if (
        is_service_hostname(ctx)
        or is_service_path(ctx)
        or is_root_path(ctx)
        or has_explicit_port(ctx)
        or is_likely_service(ctx)
    ):
        return ClassificationResult(is_service=True)

    # Then check attachment signals
    if is_filetype(ctx) or is_attachment_path(ctx) or is_likely_attachment(ctx):
        return ClassificationResult(is_service=False)

    # Default to service if no clear signals
    return ClassificationResult(is_service=True)


def classify_links(links: List[str]) -> Dict[str, List[str]]:
    """Classify URLs as either service endpoints or file attachments.

    Uses various heuristics:
    - File extensions
    - Hostname patterns
    - URL path characteristics
    - Port specifications
    - Keyword matching

    Args:
        links: List of URLs to classify.

    Returns:
        Dictionary with two keys:
        - 'attachments': List of URLs likely pointing to downloadable files
        - 'services': List of URLs likely pointing to service endpoints
    """
    attachments = []
    services = []

    for link in links:
        try:
            result = classify_url(link)
            if result.is_service:
                services.append(link)
                logger.debug(f"Classified as service: {link}")
            else:
                attachments.append(link)
                logger.debug(f"Classified as attachment: {link}")

        except Exception as e:
            logger.error(f"Failed to classify URL {link!r}: {e}")

    return {
        "attachments": attachments,
        "services": services,
    }
