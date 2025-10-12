import httpx
from urllib.parse import urlparse

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.models.capability import Capabilities
from ctfbridge.platforms.cryptohack.services.challenge import CryptoHackChallengeService
from ctfbridge.platforms.cryptohack.services.auth import CryptoHackAuthService


class CryptoHackClient(CoreCTFClient):
    @property
    def capabilities(self) -> Capabilities:
        return Capabilities(view_challenges=True, login=True, submit_flags=True)

    def __init__(self, http: httpx.AsyncClient, url: str):
        self._platform_url = "https://cryptohack.org"
        self._http = http

        path = urlparse(url).path.strip("/")
        parts = [p for p in path.split("/") if p]
        if len(parts) == 2 and parts[0] == "challenges":
            self.category_from_url = parts[1]
        else:
            self.category_from_url = None

        super().__init__(
            session=CoreSessionHelper(self),
            attachments=CoreAttachmentService(self),
            auth=CryptoHackAuthService(self),
            challenges=CryptoHackChallengeService(self),
            scoreboard=None,
        )

    @property
    def platform_name(self) -> str:
        return "CryptoHack"

    @property
    def platform_url(self) -> str:
        return self._platform_url
