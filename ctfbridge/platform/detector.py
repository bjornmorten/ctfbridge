from typing import Optional
from urllib.parse import urlparse, urlunparse

import requests

from ..exceptions import UnknownBaseURL, UnknownPlatformError
from .matchers import PLATFORM_MATCHERS


def generate_candidate_base_urls(full_url: str) -> list[str]:
    parsed = urlparse(full_url)

    if not parsed.path.strip("/"):
        return [urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))]

    parts = parsed.path.strip("/").split("/")
    candidates = []

    for i in range(len(parts), -1, -1):
        path = "/" + "/".join(parts[:i]) if i > 0 else ""
        candidate = urlunparse((parsed.scheme, parsed.netloc, path.rstrip("/"), "", "", ""))
        candidates.append(candidate)

    return candidates

def detect_platform(input_url: str) -> tuple[str, str]:
    if input_url.strip() == "demo":
        return "demo", "demo"

    candidates = generate_candidate_base_urls(input_url)

    platform_matcher = None
    while not platform_matcher and candidates and (candidate := candidates.pop()):
        response = requests.get(candidate)
        for matcher in PLATFORM_MATCHERS:
            if matcher.matches(response):
                platform_matcher = matcher

    if not platform_matcher:
        raise UnknownPlatformError(f"Could not detect platform from {input_url}")

    while candidate:
        if platform_matcher.is_base_url(candidate):
            return platform_matcher.name, candidate

        if not candidates:
            break

        candidate = candidates.pop()
        
    raise UnknownBaseURL(f"Could not find base URL from {input_url}")
