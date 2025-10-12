import httpx
from urllib.parse import urlparse

from ctfbridge.core.client import CoreCTFClient
from ctfbridge.platforms.pwncollege.services.attachment import PwnCollegeAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.models.capability import Capabilities
from ctfbridge.platforms.pwncollege.services.challenge import PwnCollegeChallengeService
from ctfbridge.platforms.ctfd.services.auth import CTFdAuthService


class PwnCollegeClient(CoreCTFClient):
    @property
    def capabilities(self) -> Capabilities:
        return Capabilities(view_challenges=True, login=True, submit_flags=True)

    def __init__(self, http: httpx.AsyncClient, url: str):
        self._platform_url = "https://pwn.college"
        self._http = http

        path = urlparse(url).path.strip("/")
        parts = [p for p in path.split("/") if p]

        if len(parts) == 0:
            # Base URL — no dojo/module
            self.dojo_slug = None
            self.module_slug = None
        elif len(parts) == 1:
            # /<dojo>
            self.dojo_slug = parts[0]
            self.module_slug = None
        elif len(parts) == 2:
            # /<dojo>/<module>
            self.dojo_slug, self.module_slug = parts
        else:
            # Invalid path
            raise ValueError(f"Unexpected URL format: {url}")

        super().__init__(
            session=CoreSessionHelper(self),
            attachments=PwnCollegeAttachmentService(self),
            auth=CTFdAuthService(self),
            challenges=PwnCollegeChallengeService(self),
            scoreboard=None,
        )

    @property
    def platform_name(self) -> str:
        return "pwn.college"

    @property
    def platform_url(self) -> str:
        return self._platform_url
