import httpx

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.platforms.ctfd.services.auth import CTFdAuthService
from ctfbridge.platforms.ctfd.services.challenge import CTFdChallengeService
from ctfbridge.platforms.ctfd.services.scoreboard import CTFdScoreboardService
from ctfbridge.models.capability import Capabilities


class CTFdClient(CoreCTFClient):
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
            auth=CTFdAuthService(self),
            challenges=CTFdChallengeService(self),
            scoreboard=CTFdScoreboardService(self),
        )

    @property
    def platform_name(self) -> str:
        return "CTFd"

    @property
    def platform_url(self) -> str:
        return self._platform_url
