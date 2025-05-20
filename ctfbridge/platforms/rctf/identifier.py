import httpx

from ctfbridge.base.identifier import PlatformIdentifier
from ctfbridge.exceptions import UnauthorizedError


class RCTFIdentifier(PlatformIdentifier):
    """
    Identifier for RCTF platforms.

    Uses known API endpoints to verify whether a given base URL is a RCTF instance.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    async def static_detect(self, response: httpx.Response) -> bool:
        return "rctf-config" in response.text

    async def dynamic_detect(self, base_url: str) -> bool:
        return False

    async def is_base_url(self, candidate: str) -> bool:
        try:
            await self.http.get(f"{candidate}/api/v1/users/me")
        except UnauthorizedError as e:
            return str(e) == "The token provided is invalid."
        except (httpx.HTTPError, ValueError):
            return False
