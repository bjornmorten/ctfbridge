import logging
from urllib.parse import urljoin, urlparse, urlunparse

logger = logging.getLogger(__name__)


def generate_candidate_base_urls(url: str) -> list[str]:
    """
    Given a full URL, generate a list of parent path candidates,
    ordered from most specific to root.

    Example:
        input:  https://example.com/foo/bar/challenges
        output: [
            https://example.com/foo/bar/challenges,
            https://example.com/foo/bar,
            https://example.com/foo,
            https://example.com
        ]
    """
    logger.debug("Generating candidate base URLs for: %s", url)
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/") if parsed.path else []
    candidates = []

    for i in range(len(path_parts), -1, -1):
        path = "/" + "/".join(path_parts[:i]) if i > 0 else ""
        candidate = urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))
        candidates.append(candidate)

    logger.debug("Generated candidates for %s: %s", url, candidates)
    return candidates


def normalize_url(url: str) -> str:
    """
    Normalize a URL by stripping trailing slashes and fragments.
    """
    logger.debug("Normalizing URL: %s", url)
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    normalized = urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))
    logger.debug("Normalized %s to %s", url, normalized)


def get_base_netloc(url: str) -> str:
    """
    Extract scheme and host from a URL (e.g., https://example.com).
    """
    logger.debug("Getting base netloc for URL: %s", url)
    parsed = urlparse(url)
    base_netloc = f"{parsed.scheme}://{parsed.netloc}"
    logger.debug("Base netloc for %s is %s", url, base_netloc)
    return base_netloc


def is_same_origin(url1: str, url2: str) -> bool:
    """
    Check if two URLs share the same scheme and netloc.
    """
    logger.debug("Checking if URLs are same origin: %s and %s", url1, url2)
    origin1 = get_base_netloc(url1)
    origin2 = get_base_netloc(url2)
    result = origin1 == origin2
    logger.debug("Same origin result for %s and %s: %s", url1, url2, result)
    return result


def resolve_relative(base_url: str, relative_path: str) -> str:
    """
    Resolve a relative path or endpoint against a base URL.
    Useful for constructing API requests from base URLs.
    """
    logger.debug(
        "Resolving relative path. Base URL: %s, Relative path: %s", base_url, relative_path
    )

    if not base_url.endswith("/"):
        base_url_with_slash = base_url + "/"
    else:
        base_url_with_slash = base_url

    resolved_url = urljoin(base_url_with_slash, relative_path.lstrip("/"))
    logger.debug(
        "Resolved URL for base %s and relative %s: %s", base_url, relative_path, resolved_url
    )
    return resolved_url
