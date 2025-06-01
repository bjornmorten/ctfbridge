from typing import Optional

from urllib.parse import ParseResult
import httpx

from ctfbridge.base.identifier import PlatformIdentifier
from ctfbridge.exceptions import UnauthorizedError


class RCTFIdentifier(PlatformIdentifier):
    """
    Identifier for rCTF platforms using known API endpoints and response signatures.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    def platform_name(self) -> str:
        """
        Get the platform name.
        """
        return "rCTF"

    def match_url_pattern(self, url: ParseResult) -> bool:
        return False

    async def static_detect(self, response: httpx.Response) -> Optional[bool]:
        """
        Lightweight static detection by checking HTML or response text for rCTF signatures.
        """
        if "rctf-config" in response.text:
            return True
        return None

    async def is_base_url(self, candidate: str) -> bool:
        """
        A base URL is valid if the rCTF /api/v1/users/me endpoint returns the expected
        unauthorized error message.
        """
        try:
            res = await self.http.get(f"{candidate}/api/v1/users/me")
            return "badToken" in res.text
        except (httpx.HTTPError, ValueError):
            return False
        return False

    async def dynamic_detect(self, base_url: str) -> bool:
        """
        Confirm platform identity by checking known rCTF API response signature.
        Currently not implemented as static detection is sufficient.
        """
        return False
