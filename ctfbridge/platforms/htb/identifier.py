import re

import httpx

from ctfbridge.base.identifier import PlatformIdentifier


class HTBIdentifier(PlatformIdentifier):
    """
    Identifier for HTB platforms.

    Uses known API endpoints to verify whether a given base URL is a HTB instance.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    async def static_detect(self, response: httpx.Response) -> bool:
        return response.url.host == "ctf.hackthebox.com"

    async def dynamic_detect(self, base_url: str) -> bool:
        return False

    async def is_base_url(self, candidate: str) -> bool:
        pattern = r"^https://ctf\.hackthebox\.com/event/\d+$"
        return bool(re.match(pattern, candidate))
