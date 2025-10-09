from urllib.parse import ParseResult, urlparse

import httpx

from ctfbridge.base.identifier import PlatformIdentifier
from ctfbridge.platforms.ept.http.endpoints import Endpoints


class CryptoHackIdentifier(PlatformIdentifier):
    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    def platform_name(self):
        return "CryptoHack"

    def match_url_pattern(self, url: ParseResult) -> bool:
        return url.netloc.lower() == "cryptohack.org"

    async def static_detect(self, response: httpx.Response) -> bool | None:
        return False

    async def dynamic_detect(self, base_url: str) -> bool:
        return False

    async def is_base_url(self, candidate: str) -> bool:
        return urlparse(candidate).path.strip("/") == ""
