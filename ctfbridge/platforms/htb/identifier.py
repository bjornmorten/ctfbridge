from typing import Optional
import re

import httpx

from ctfbridge.base.identifier import PlatformIdentifier


class HTBIdentifier(PlatformIdentifier):
    """
    Identifier for HTB platforms using known API endpoints and response signatures.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    def platform_name(self) -> str:
        """
        Get the platform name.
        """
        return "HTB"

    def match_url_pattern(self, url: str) -> bool:
        """
        Quick check for common HTB URLs.
        """
        return "hackthebox" in url.lower()

    async def static_detect(self, response: httpx.Response) -> Optional[bool]:
        """
        Lightweight static detection by checking if the URL matches HTB's domain.
        """
        if response.url.host == "ctf.hackthebox.com":
            return True
        return None

    async def dynamic_detect(self, base_url: str) -> bool:
        """
        Confirm platform identity by checking known HTB API response signature.
        Currently not implemented as static detection is sufficient.
        """
        return False

    async def is_base_url(self, candidate: str) -> bool:
        """
        A base URL is valid if it matches the HTB event URL pattern.
        """
        pattern = r"^https://ctf\.hackthebox\.com/event/\d+$"
        return bool(re.match(pattern, candidate))
