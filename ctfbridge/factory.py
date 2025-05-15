import httpx
from ctfbridge.platforms.detect import detect_platform
from ctfbridge.base.client import CTFClient
from ctfbridge.platforms import get_platform_client
from ctfbridge.exceptions import UnknownPlatformError
from ctfbridge.utils.platform_cache import get_cached_platform, set_cached_platform
from ctfbridge.core.http import make_http_client


async def create_client(
    url: str,
    *,
    platform: str = "auto",
    verify_ssl: bool = True,
    cache_platform: bool = True,
    http: httpx.AsyncClient | None = None,
) -> CTFClient:
    """
    Create and return a resolved CTF client.

    Args:
        url: Full or base URL of the platform.
        platform: Platform name or 'auto'.
        verify_ssl: Whether to verify SSL certs.
        cache_platform: Whether to cache platform detection.
        http: Optional preconfigured HTTP client.

    Returns:
        A resolved and ready-to-use CTFClient instance.
    """
    http = http or make_http_client()

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

    try:
        client_class = get_platform_client(platform)
    except UnknownPlatformError:
        raise UnknownPlatformError(platform)

    return client_class(http=http, url=base_url)
