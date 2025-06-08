import httpx

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.platforms.ept.services.auth import EPTAuthService
from ctfbridge.platforms.ept.services.challenge import EPTChallengeService
from ctfbridge.platforms.ept.services.scoreboard import EPTScoreboardService
from ctfbridge.models.capability import Capabilities


class EPTClient(CoreCTFClient):
    @property
    def capabilities(self) -> Capabilities:
        return Capabilities(
            login=True,
            submit_flag=True,
            view_challenges=True,
            view_scoreboard=True,
        )

    def __init__(self, http: httpx.AsyncClient, url: str):
        self._platform_url = url
        self._http = http

        super().__init__(
            session=CoreSessionHelper(self),
            attachments=CoreAttachmentService(self),
            auth=EPTAuthService(self),
            challenges=EPTChallengeService(self),
            scoreboard=EPTScoreboardService(self),
        )

    @property
    def platform_url(self) -> str:
        return self._platform_url
