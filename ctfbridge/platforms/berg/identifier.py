from typing import Optional

from urllib.parse import ParseResult

import httpx

from ctfbridge.base.identifier import PlatformIdentifier


class BergIdentifier(PlatformIdentifier):
    """
    Identifier for Berg platforms using known API endpoints and response signatures.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    def platform_name(self) -> str:
        """
        Get the platform name.
        """
        return "Berg"

    def match_url_pattern(self, url: ParseResult) -> bool:
        return False

    async def static_detect(self, response: httpx.Response) -> Optional[bool]:
        """
        Lightweight static detection by checking HTML or response text for Berg signatures.
        """
        return None

    async def dynamic_detect(self, base_url: str) -> bool:
        """
        Confirm platform identity by checking known Berg API response signature.
        """
        try:
            resp = await self.http.get(f"{base_url}/api/v2/metadata")
            return "challengeSolvesBeforeMinimum" in resp.text
        except (httpx.HTTPError, ValueError):
            return False

    async def is_base_url(self, candidate: str) -> bool:
        """
        A base URL is valid if the Berg metadata endpoint returns the expected response.
        """
        try:
            resp = await self.http.get(f"{candidate}/api/v2/metadata")
            return "challengeSolvesBeforeMinimum" in resp.text
        except (httpx.HTTPError, ValueError):
            return False
