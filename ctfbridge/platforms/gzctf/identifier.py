import re
from urllib.parse import ParseResult, urlparse

import httpx

from ctfbridge.base.identifier import PlatformIdentifier
from ctfbridge.platforms.ept.http.endpoints import Endpoints


class GZCTFIdentifier(PlatformIdentifier):
    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    def platform_name(self):
        return "GZCTF"

    def match_url_pattern(self, url: ParseResult) -> bool:
        return False

    async def static_detect(self, response: httpx.Response) -> bool | None:
        if "GZCTF" in response.text or "GZ::CTF" in response.text:
            return True
        return None

    async def dynamic_detect(self, base_url: str) -> bool:
        return False

    async def is_base_url(self, candidate: str) -> bool:
        pattern = r"^/games/\d+$"
        path = urlparse(candidate).path
        return bool(re.match(pattern, path))
