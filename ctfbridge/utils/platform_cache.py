import json
import time
from pathlib import Path
from typing import Optional

CACHE_PATH = Path.home() / ".ctfbridge_platform_cache.json"
CACHE_TTL_SECONDS = 86400

CacheEntry = tuple[str, str, float]
CacheMap = dict[str, CacheEntry]


def load_platform_cache() -> CacheMap:
    """
    Load the platform cache from disk.

    Returns:
        A dictionary mapping URLs to (platform, base_url, timestamp).
        Returns an empty dict if the file does not exist or is invalid.
    """
    if not CACHE_PATH.exists():
        return {}
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            raw = json.load(f)
            return {k: tuple(v) for k, v in raw.items()}
    except (json.JSONDecodeError, TypeError, ValueError):
        return {}


def save_platform_cache(cache: CacheMap) -> None:
    """
    Save the platform cache to disk.

    Args:
        cache: The cache dictionary mapping URLs to (platform, base_url, timestamp).
    """
    serializable_cache = {k: list(v) for k, v in cache.items()}
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(serializable_cache, f, indent=2)


def get_cached_platform(url: str) -> Optional[tuple[str, str]]:
    """
    Get a cached platform and base URL for the given input URL, if the cache entry is valid.

    Args:
        url: The original user-provided platform URL.

    Returns:
        A tuple (platform, base_url) if a non-expired cache entry is found; None otherwise.
    """
    cache = load_platform_cache()
    entry = cache.get(url)

    if not entry:
        return None

    platform, base_url, timestamp = entry
    if time.time() - timestamp > CACHE_TTL_SECONDS:
        # Expired cache entry
        cache.pop(url)
        save_platform_cache(cache)
        return None

    return platform, base_url


def set_cached_platform(url: str, platform: str, base_url: str) -> None:
    """
    Store the platform and base URL in the cache with the current timestamp.

    Args:
        url: The original user-provided URL (lookup key).
        platform: Detected platform name (e.g., 'ctfd').
        base_url: Cleaned and confirmed base URL for the platform.
    """
    cache = load_platform_cache()
    cache[url] = (platform, base_url, time.time())
    save_platform_cache(cache)
