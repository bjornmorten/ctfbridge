import httpx

from ctfbridge.base.identifier import PlatformIdentifier


class CTFdIdentifier(PlatformIdentifier):
    """
    Identifier for CTFd platforms.

    Uses known API endpoints to verify whether a given base URL is a CTFd instance.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    async def static_detect(self, response: httpx.Response) -> bool:
        return "ctfd" in response.text or "CTFd" in response.text

    async def dynamic_detect(self, base_url: str) -> bool:
        try:
            url = f"{base_url}/api/v1/swagger.json"
            resp = await self.http.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return "Endpoint to disband your current team. Can only" in data
        except (httpx.HTTPError, ValueError):
            pass
        return False

    async def is_base_url(self, candidate: str) -> bool:
        try:
            url = f"{candidate.rstrip('/')}/api/v1/swagger.json"
            resp = await self.http.get(url, timeout=5)
            return resp.status_code == 200
        except (httpx.HTTPError, ValueError):
            return False
