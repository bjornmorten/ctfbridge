import re
from urllib.parse import ParseResult

import httpx

from ctfbridge.base.identifier import PlatformIdentifier


class HTBIdentifier(PlatformIdentifier):
    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    def platform_name(self):
        return "HTB"

    def match_url_pattern(self, url: ParseResult) -> bool:
        return url.netloc.lower() == "ctf.hackthebox.com"

    async def static_detect(self, response: httpx.Response) -> bool | None:
        return False

    async def dynamic_detect(self, base_url: str) -> bool:
        return False

    async def is_base_url(self, candidate: str) -> bool:
        pattern = r"^https://ctf\.hackthebox\.com/event/\d+$"
        return bool(re.match(pattern, candidate))
