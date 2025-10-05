from ctfbridge.utils.url import get_base_netloc

import httpx

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.models.capability import Capabilities
from ctfbridge.platforms.htb.services.auth import HTBAuthService
from ctfbridge.platforms.htb.services.challenge import HTBChallengeService
from ctfbridge.platforms.htb.services.scoreboard import HTBScoreboardService


class HTBClient(CoreCTFClient):
    @property
    def capabilities(self) -> Capabilities:
        return Capabilities(
            login=True, view_challenges=True, submit_flags=True, view_scoreboard=True
        )

    def __init__(self, http: httpx.AsyncClient, url: str):
        self._http = http

        self._ctf_id = url.split("/")[-1]
        self._platform_url = get_base_netloc(url)

        super().__init__(
            session=CoreSessionHelper(self),
            attachments=CoreAttachmentService(self),
            auth=HTBAuthService(self),
            challenges=HTBChallengeService(self),
            scoreboard=HTBScoreboardService(self),
        )

    @property
    def platform_name(self) -> str:
        return "HTB"

    @property
    def platform_url(self) -> str:
        return self._platform_url
