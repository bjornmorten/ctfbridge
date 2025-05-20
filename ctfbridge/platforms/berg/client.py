import httpx

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.platforms.berg.services.auth import BergAuthService
from ctfbridge.platforms.berg.services.challenge import BergChallengeService
from ctfbridge.platforms.berg.services.scoreboard import BergScoreboardService
from ctfbridge.platforms.registry import platform


@platform("berg")
class BergClient(CoreCTFClient):
    def __init__(self, http: httpx.AsyncClient, url: str):
        self._platform_url = url
        self._http = http

        super().__init__(
            session=CoreSessionHelper(self),
            attachments=CoreAttachmentService(self),
            auth=BergAuthService(self),
            challenges=BergChallengeService(self),
            scoreboard=BergScoreboardService(self),
        )

    @property
    def platform_url(self) -> str:
        return self._platform_url
