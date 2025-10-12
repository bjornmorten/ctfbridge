from urllib.parse import ParseResult, urlparse

import httpx

from ctfbridge.base.identifier import PlatformIdentifier


class PwnCollegeIdentifier(PlatformIdentifier):
    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    def platform_name(self):
        return "pwn.college"

    def match_url_pattern(self, url: ParseResult) -> bool:
        return url.netloc.lower() == "pwn.college"

    async def static_detect(self, response: httpx.Response) -> bool | None:
        return False

    async def dynamic_detect(self, base_url: str) -> bool:
        return False

    async def is_base_url(self, candidate: str) -> bool:
        # TODO: verify that the paths actually are dojos/modules
        # now just checking if it is / or /<dojo> or /<dojo>/<module> based on length
        path = urlparse(candidate).path.strip("/")
        parts = [p for p in path.split("/") if p]
        return len(parts) in (0, 1, 2)
