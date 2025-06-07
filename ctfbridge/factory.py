import httpx
import logging
from typing import Any

from ctfbridge.base.client import CTFClient
from ctfbridge.core.http import make_http_client
from ctfbridge.exceptions import UnknownPlatformError

logger = logging.getLogger(__name__)


async def create_client(
    url: str,
    *,
    platform: str = "auto",
    cache_platform: bool = True,
    http: httpx.AsyncClient | None = None,
    http_config: dict[str, Any] = {},
) -> CTFClient:
    """
    Create and return a resolved CTF client.

    Args:
        url: Full or base URL of the platform.
        platform: Platform name or 'auto'.
        cache_platform: Whether to cache platform detection.
        http: Optional preconfigured HTTP client.
        http_config: Configuration dictionary for the HTTP client with options:
            - timeout: Request timeout in seconds (int/float)
            - retries: Number of retries for failed requests (int)
            - max_connections: Maximum number of concurrent connections (int)
            - http2: Whether to enable HTTP/2 (bool)
            - auth: Authentication credentials (tuple/httpx.Auth)
            - event_hooks: Request/response event hooks (dict)
            - verify_ssl: Whether to verify SSL certificates (bool)
            - headers: Custom HTTP headers (dict)
            - proxy: Proxy configuration (dict/str)
            - user_agent: Custom User-Agent string (str)

    Returns:
        A resolved and ready-to-use CTFClient instance.
    """
    from ctfbridge.platforms import get_platform_client
    from ctfbridge.platforms.detect import detect_platform
    from ctfbridge.utils.platform_cache import get_cached_platform, set_cached_platform

    logger.info(f"Initializing CTFBridge client for URL: {url} (Specified platform: {platform})")

    http = http or make_http_client(config=http_config)

    if platform == "auto":
        logger.debug(f"Attempting to auto-detect platform for {url}.")
        if cache_platform:
            cached = get_cached_platform(url)
            if cached:
                platform, base_url = cached
                logger.debug(
                    f"Platform cache hit for {url}: Platform={platform}, Base URL={base_url}"
                )
            else:
                logger.debug(f"Platform cache miss for {url}. Detecting platform...")
                platform, base_url = await detect_platform(url, http)
                logger.debug(f"Platform detected: Name={platform}, Base URL={base_url}")
                set_cached_platform(url, platform, base_url)
        else:
            platform, base_url = await detect_platform(url, http)
            logger.debug(f"Platform detected (no cache): Name={platform}, Base URL={base_url}")
    else:
        base_url = url
        logger.debug(f"Using specified platform: Name={platform}, Base URL={base_url}")

    try:
        client_class = get_platform_client(platform)
    except UnknownPlatformError:
        logger.error(f"Unknown platform specified or detected: {platform}")
        raise UnknownPlatformError(platform)

    initialized_client = client_class(http=http, url=base_url)
    logger.info(
        f"CTFBridge client for {initialized_client.platform_name} at {initialized_client.platform_url} created successfully."
    )
    return initialized_client
