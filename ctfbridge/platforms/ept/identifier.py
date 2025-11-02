from typing import Optional
from urllib.parse import ParseResult

import httpx

from ctfbridge.base.identifier import PlatformIdentifier
from ctfbridge.platforms.ept.http.endpoints import Endpoints


class EPTIdentifier(PlatformIdentifier):
    """
    Identifier for EPT platforms using known API endpoints and response signatures.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    def platform_name(self):
        return "EPT"

    def match_url_pattern(self, url: ParseResult) -> bool:
        return url.netloc.lower() == "backend.ept.gg"

    async def static_detect(self, response: httpx.Response) -> bool | None:
        return None

    async def is_base_url(self, candidate: str) -> bool:
        try:
            url = f"{candidate.rstrip('/')}{Endpoints.Misc.METADATA}"
            resp = await self.http.get(url, timeout=5)
            return resp.status_code == 200
        except (httpx.HTTPError, ValueError):
            return False

    async def dynamic_detect(self, base_url: str) -> bool:
        try:
            url = f"{base_url.rstrip('/')}{Endpoints.Misc.METADATA}"
            resp = await self.http.get(url, timeout=5)

            if resp.status_code == 200 and "anonymous_allowed" in resp.text:
                return True
        except (httpx.HTTPError, ValueError):
            pass
        return False
