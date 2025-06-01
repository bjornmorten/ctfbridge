from typing import Optional

from urllib.parse import ParseResult

import httpx

from ctfbridge.base.identifier import PlatformIdentifier


class EPTIdentifier(PlatformIdentifier):
    """
    Identifier for EPT platforms using known API endpoints and response signatures.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    def platform_name(self) -> str:
        """
        Get the platform name.
        """
        return "EPT"

    def match_url_pattern(self, url: ParseResult) -> bool:
        return False

    async def static_detect(self, response: httpx.Response) -> Optional[bool]:
        """
        Lightweight static detection by checking HTML or response text for EPT signatures.
        """
        return None

    async def dynamic_detect(self, base_url: str) -> bool:
        """
        Confirm platform identity by checking known EPT API response signature.
        """
        try:
            resp = await self.http.get(f"{base_url}/api/metadata")
            return resp.status_code == 200 and "divisions" in resp.text
        except (httpx.HTTPError, ValueError):
            return False

    async def is_base_url(self, candidate: str) -> bool:
        """
        A base URL is valid if the EPT metadata endpoint returns the expected response.
        """
        try:
            resp = await self.http.get(f"{candidate}/api/metadata")
            return resp.status_code == 200 and "divisions" in resp.text
        except (httpx.HTTPError, ValueError):
            return False
