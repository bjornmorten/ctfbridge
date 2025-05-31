import httpx
from typing import Any

from ctfbridge.base.client import CTFClient
from ctfbridge.core.http import make_http_client
from ctfbridge.exceptions import UnknownPlatformError


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

    http = http or make_http_client(config=http_config)

    if platform == "auto":
        if cache_platform:
            cached = get_cached_platform(url)
            if cached:
                platform, base_url = cached
            else:
                platform, base_url = await detect_platform(url, http)
                set_cached_platform(url, platform, base_url)
        else:
            platform, base_url = await detect_platform(url, http)
    else:
        base_url = url

    try:
        client_class = get_platform_client(platform)
    except UnknownPlatformError:
        raise UnknownPlatformError(platform)

    return client_class(http=http, url=base_url)
