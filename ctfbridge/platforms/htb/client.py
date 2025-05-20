from urllib.parse import urljoin

import httpx

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.platforms.htb.services.auth import HTBAuthService
from ctfbridge.platforms.htb.services.challenge import HTBChallengeService
from ctfbridge.platforms.htb.services.scoreboard import HTBScoreboardService
from ctfbridge.platforms.registry import platform


@platform("htb")
class HTBClient(CoreCTFClient):
    def __init__(self, http: httpx.AsyncClient, url: str):
        self._platform_url = url
        self._http = http

        super().__init__(
            session=CoreSessionHelper(self),
            attachments=CoreAttachmentService(self),
            auth=HTBAuthService(self),
            challenges=HTBChallengeService(self),
            scoreboard=HTBScoreboardService(self),
        )

    @property
    def platform_url(self) -> str:
        return self._platform_url

    @property
    def _ctf_id(self) -> str:
        return self._platform_url.split("/")[-1]

    def _get_api_url(self, endpoint: str) -> str:
        path = endpoint.format()
        full_url = urljoin("https://ctf.hackthebox.com/api/", path)
        return full_url
