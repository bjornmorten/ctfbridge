from typing import Tuple
from urllib.parse import urlparse, urlunparse

import httpx

from ctfbridge.exceptions import UnknownBaseURLError, UnknownPlatformError
from ctfbridge.platforms.registry import get_identifier_classes


def generate_candidate_base_urls(full_url: str) -> list[str]:
    parsed = urlparse(full_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {full_url}")

    parts = parsed.path.strip("/").split("/") if parsed.path.strip("/") else []
    candidates = []

    for i in range(len(parts), -1, -1):
        path = "/" + "/".join(parts[:i]) if i > 0 else ""
        candidate = urlunparse((parsed.scheme, parsed.netloc, path.rstrip("/"), "", "", ""))
        candidates.append(candidate)

    return candidates


async def detect_platform(input_url: str, http: httpx.AsyncClient) -> Tuple[str, str]:
    """
    Detect the platform type and base URL from a possibly nested URL.

    Args:
        input_url: The full input URL to platform.
        http: A shared HTTP client.

    Returns:
        Platform name and platform base URL

    Raises:
        UnknownPlatformError: If no known platform is matched.
        UnknownBaseURL: If the platform is matched but no working base URL is found.
    """
    identifiers = get_identifier_classes()
    candidates = generate_candidate_base_urls(input_url)

    async def _find_valid_base_url(identifier, candidates):
        for base_candidate in candidates:
            if await identifier.is_base_url(base_candidate):
                return base_candidate
        raise UnknownBaseURLError(input_url)

    # Step 0: Try static detection for each candidate
    parsed_url = urlparse(input_url)
    for name, IdentifierClass in identifiers:
        identifier = IdentifierClass(http)
        if identifier.match_url_pattern(parsed_url):
            base_url = await _find_valid_base_url(identifier, candidates)
            return name, base_url

    # Step 1: Try static detection for each candidate
    for candidate in candidates:
        try:
            resp = await http.get(candidate, timeout=5)
        except httpx.HTTPError:
            continue

        for name, IdentifierClass in identifiers:
            identifier = IdentifierClass(http)
            if await identifier.static_detect(resp):
                base_url = await _find_valid_base_url(identifier, candidates)
                return name, base_url

    # Step 2: Fallback to dynamic detection
    for candidate in candidates:
        for name, IdentifierClass in identifiers:
            identifier = IdentifierClass(http)
            if await identifier.dynamic_detect(candidate):
                base_url = await _find_valid_base_url(identifier, candidates)
                return name, base_url

    raise UnknownPlatformError(f"Could not detect platform from {input_url}")
