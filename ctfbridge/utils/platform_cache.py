import json
import tempfile
import time
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

CACHE_PATH = Path(tempfile.gettempdir()) / ".ctfbridge_platform_cache.json"
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
        logger.debug("Platform cache file not found at %s.", CACHE_PATH)
        return {}
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            raw = json.load(f)
            return {k: tuple(v) for k, v in raw.items()}
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        logger.warning(
            "Failed to load or parse platform cache from %s: %s. Returning empty cache.",
            CACHE_PATH,
            e,
        )
        return {}


def save_platform_cache(cache: CacheMap) -> None:
    """
    Save the platform cache to disk.

    Args:
        cache: The cache dictionary mapping URLs to (platform, base_url, timestamp).
    """
    serializable_cache = {k: list(v) for k, v in cache.items()}
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(serializable_cache, f, indent=2)
        logger.debug("Platform cache saved successfully to %s.", CACHE_PATH)
    except OSError as e:
        logger.error("Failed to save platform cache to %s: %s", CACHE_PATH, e)


def get_cached_platform(url: str) -> Optional[tuple[str, str]]:
    """
    Get a cached platform and base URL for the given input URL, if the cache entry is valid.

    Args:
        url: The original user-provided platform URL.

    Returns:
        A tuple (platform, base_url) if a non-expired cache entry is found; None otherwise.
    """
    logger.debug("Checking platform cache for URL: %s.", url)
    cache = load_platform_cache()
    entry = cache.get(url)

    if not entry:
        logger.debug("Cache miss for URL: %s.", url)
        return None

    platform, base_url, timestamp = entry
    if time.time() - timestamp > CACHE_TTL_SECONDS:
        logger.debug(
            "Cache entry for URL %s is expired (Timestamp: %s, TTL: %s).",
            url,
            timestamp,
            CACHE_TTL_SECONDS,
        )
        # Removing expired cache entry
        cache.pop(url)
        save_platform_cache(cache)
        return None

    logger.debug("Cache hit for URL %s: Platform=%s, Base URL=%s.", url, platform, base_url)
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
    logger.debug("Cached platform for URL %s: Platform=%s, Base URL=%s.", url, platform, base_url)
