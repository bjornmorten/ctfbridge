import httpx

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.models.capability import Capabilities
from ctfbridge.platforms.berg.services.challenge import BergChallengeService


class BergClient(CoreCTFClient):
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
            challenges=BergChallengeService(self),
            scoreboard=None,
        )

    @property
    def platform_name(self) -> str:
        return "Berg"

    @property
    def platform_url(self) -> str:
        return self._platform_url
