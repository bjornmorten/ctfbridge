import httpx

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.platforms.rctf.services.auth import RCTFAuthService
from ctfbridge.platforms.rctf.services.challenge import RCTFChallengeService
from ctfbridge.platforms.rctf.services.scoreboard import RCTFScoreboardService
from ctfbridge.platforms.registry import platform


@platform("rctf")
class RCTFClient(CoreCTFClient):
    def __init__(self, http: httpx.AsyncClient, url: str):
        self._platform_url = url
        self._http = http

        super().__init__(
            session=CoreSessionHelper(self),
            attachments=CoreAttachmentService(self),
            auth=RCTFAuthService(self),
            challenges=RCTFChallengeService(self),
            scoreboard=RCTFScoreboardService(self),
        )

    @property
    def platform_url(self) -> str:
        return self._platform_url
