from typing import Optional

import httpx
from urllib.parse import ParseResult

from ctfbridge.base.identifier import PlatformIdentifier
from ctfbridge.platforms.ctfd.http.endpoints import Endpoints


class CTFdIdentifier(PlatformIdentifier):
    """
    Identifier for CTFd platforms using known API endpoints and response signatures.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    def platform_name(self):
        return "CTFd"

    def match_url_pattern(self, url: ParseResult) -> bool:
        return url.netloc.lower().endswith(".ctfd.io")

    async def static_detect(self, response: httpx.Response) -> Optional[bool]:
        """
        Lightweight static detection by checking HTML or response text for 'ctfd'.
        """
        text = response.text
        if "Powered by CTFd" in text:
            return True
        return None

    async def is_base_url(self, candidate: str) -> bool:
        """
        A base URL is valid if the CTFd /api/v1/swagger endpoint is reachable.
        """
        try:
            url = f"{candidate.rstrip('/')}{Endpoints.Misc.SWAGGER}"
            resp = await self.http.get(url, timeout=5)
            return resp.status_code == 200
        except (httpx.HTTPError, ValueError):
            return False

    async def dynamic_detect(self, base_url: str) -> bool:
        """
        Confirm platform identity by checking known CTFd API response signature.
        """
        try:
            url = f"{base_url.rstrip('/')}{Endpoints.Misc.SWAGGER}"
            resp = await self.http.get(url, timeout=5)

            if resp.status_code == 200 and "disband your current team" in resp.text:
                return True
        except (httpx.HTTPError, ValueError):
            pass
        return False
