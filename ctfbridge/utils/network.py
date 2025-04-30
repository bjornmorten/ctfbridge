from urllib.parse import urlparse


def is_external_url(base_url: str, target_url: str) -> bool:
    """Return True if target_url points to a different domain than base_url."""
    base_netloc = urlparse(base_url).netloc
    target_netloc = urlparse(target_url).netloc
    return base_netloc != target_netloc
