from urllib.parse import urlparse

import httpx

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.models.capability import Capabilities
from ctfbridge.platforms.gzctf.services.auth import GZCTFAuthService
from ctfbridge.platforms.gzctf.services.challenge import GZCTFChallengeService
from ctfbridge.platforms.gzctf.services.scoreboard import GZCTFScoreboardService


class GZCTFClient(CoreCTFClient):
    @property
    def capabilities(self) -> Capabilities:
        return Capabilities(
            login=True, view_challenges=True, submit_flags=True, view_scoreboard=True
        )

    def __init__(self, http: httpx.AsyncClient, url: str):
        self._http = http

        # get the CTF id from path (e.g. /games/1)
        parsed = urlparse(url)
        self._ctf_id = int(parsed.path.strip("/").split("/")[-1])
        self._platform_url = (
            f"{parsed.scheme}://{parsed.netloc}"  # store the platform url without the game path
        )

        super().__init__(
            session=CoreSessionHelper(self),
            attachments=CoreAttachmentService(self),
            auth=GZCTFAuthService(self),
            challenges=GZCTFChallengeService(self),
            scoreboard=GZCTFScoreboardService(self),
        )

    @property
    def platform_name(self) -> str:
        return "GZCTF"

    @property
    def platform_url(self) -> str:
        return self._platform_url
