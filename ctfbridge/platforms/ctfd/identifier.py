import httpx

from ctfbridge.base.identifier import PlatformIdentifier
from ctfbridge.platforms.ctfd.endpoints import ENDPOINTS


class CTFdIdentifier(PlatformIdentifier):
    """
    Identifier for CTFd platforms using known API endpoints and response signatures.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    async def static_detect(self, response: httpx.Response) -> bool:
        return "ctfd" in response.text.lower()

    async def dynamic_detect(self, base_url: str) -> bool:
        try:
            url = f"{base_url.rstrip('/')}{ENDPOINTS['swagger']}"
            resp = await self.http.get(url, timeout=5)
            if resp.status_code == 200:
                return "Endpoint to disband your current team. Can only" in resp.text
        except (httpx.HTTPError, ValueError):
            pass
        return False

    async def is_base_url(self, candidate: str) -> bool:
        try:
            url = f"{candidate.rstrip('/')}{ENDPOINTS['swagger']}"
            resp = await self.http.get(url, timeout=5)
            return resp.status_code == 200
        except (httpx.HTTPError, ValueError):
            return False
