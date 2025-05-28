from urllib.parse import urljoin, urlparse, urlunparse


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
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/") if parsed.path else []
    candidates = []

    for i in range(len(path_parts), -1, -1):
        path = "/" + "/".join(path_parts[:i]) if i > 0 else ""
        candidate = urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))
        candidates.append(candidate)

    return candidates


def normalize_url(url: str) -> str:
    """
    Normalize a URL by stripping trailing slashes and fragments.
    """
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    return urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))


def get_base_netloc(url: str) -> str:
    """
    Extract scheme and host from a URL (e.g., https://example.com).
    """
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def is_same_origin(url1: str, url2: str) -> bool:
    """
    Check if two URLs share the same scheme and netloc.
    """
    return get_base_netloc(url1) == get_base_netloc(url2)


def resolve_relative(base_url: str, relative_path: str) -> str:
    """
    Resolve a relative path or endpoint against a base URL.
    Useful for constructing API requests from base URLs.
    """
    return urljoin(base_url.rstrip("/") + "/", relative_path.lstrip("/"))
