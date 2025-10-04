import httpx

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.models.capability import Capabilities
from ctfbridge.platforms.rctf.services.auth import RCTFAuthService
from ctfbridge.platforms.rctf.services.challenge import RCTFChallengeService
from ctfbridge.platforms.rctf.services.scoreboard import RCTFScoreboardService


class RCTFClient(CoreCTFClient):
    @property
    def capabilities(self) -> Capabilities:
        return Capabilities(
            login=True,
            submit_flags=True,
            view_challenges=True,
            view_scoreboard=True,
        )

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
    def platform_name(self) -> str:
        return "rCTF"

    @property
    def platform_url(self) -> str:
        return self._platform_url
