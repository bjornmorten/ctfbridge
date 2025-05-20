import httpx

from ctfbridge.base.identifier import PlatformIdentifier
from ctfbridge.platforms.registry import register_identifier


@register_identifier("berg")
class BergIdentifier(PlatformIdentifier):
    """
    Identifier for Berg platforms.

    Uses known API endpoints to verify whether a given base URL is a Berg instance.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    async def static_detect(self, response: httpx.Response) -> bool:
        return False

    async def dynamic_detect(self, base_url: str) -> bool:
        try:
            resp = await self.http.get(f"{base_url}/api/v2/metadata")
            return "challengeSolvesBeforeMinimum" in resp.text
        except (httpx.HTTPError, ValueError):
            return False

    async def is_base_url(self, candidate: str) -> bool:
        try:
            resp = await self.http.get(f"{candidate}/api/v2/metadata")
            return "challengeSolvesBeforeMinimum" in resp.text
        except (httpx.HTTPError, ValueError):
            return False
