import httpx

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.models.capability import Capabilities
from ctfbridge.platforms.pwnabletw.services.challenge import PwnableTWChallengeService


class PwnableTWClient(CoreCTFClient):
    @property
    def capabilities(self) -> Capabilities:
        return Capabilities(
            view_challenges=True,
        )

    def __init__(self, http: httpx.AsyncClient, url: str):
        self._platform_url = url
        self._http = http

        super().__init__(
            session=CoreSessionHelper(self),
            attachments=CoreAttachmentService(self),
            auth=None,
            challenges=PwnableTWChallengeService(self),
            scoreboard=None,
        )

    @property
    def platform_name(self) -> str:
        return "pwnable.tw"

    @property
    def platform_url(self) -> str:
        return self._platform_url
