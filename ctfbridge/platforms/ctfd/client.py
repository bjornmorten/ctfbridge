import httpx

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.platforms.ctfd.endpoints import ENDPOINTS
from ctfbridge.platforms.ctfd.services.auth import CTFdAuthService
from ctfbridge.platforms.ctfd.services.challenge import CTFdChallengeService
from ctfbridge.platforms.ctfd.services.scoreboard import CTFdScoreboardService


class CTFdClient(CoreCTFClient):
    def __init__(self, http: httpx.AsyncClient, url: str):
        self._platform_url = url
        self._http = http

        super().__init__(
            session=CoreSessionHelper(self),
            attachments=CoreAttachmentService(self),
            auth=CTFdAuthService(self),
            challenges=CTFdChallengeService(self),
            scoreboard=CTFdScoreboardService(self),
            endpoints=ENDPOINTS,
        )

    @property
    def platform_url(self) -> str:
        return self._platform_url
