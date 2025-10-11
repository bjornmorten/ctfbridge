from urllib.parse import ParseResult, urlparse

import httpx

from ctfbridge.base.identifier import PlatformIdentifier


class PwnableKRIdentifier(PlatformIdentifier):
    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    def platform_name(self):
        return "pwnable.kr"

    def match_url_pattern(self, url: ParseResult) -> bool:
        return url.netloc.lower() == "pwnable.kr"

    async def static_detect(self, response: httpx.Response) -> bool | None:
        return False

    async def dynamic_detect(self, base_url: str) -> bool:
        return False

    async def is_base_url(self, candidate: str) -> bool:
        return urlparse(candidate).path.strip("/") == ""
