import httpx
from ctfbridge.core.client import CoreCTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.session import CoreSessionHelper
from ctfbridge.platforms.htb.services.auth import HTBAuthService
from ctfbridge.platforms.htb.services.challenge import HTBChallengeService
from ctfbridge.platforms.htb.services.scoreboard import HTBScoreboardService
from urllib.parse import urljoin
# from urllib.parse import urljoin # Already there


class HTBClient(CoreCTFClient):
    def __init__(self, http: httpx.AsyncClient, url: str):
        self._platform_url = (
            url  # This is the event-specific URL, e.g., https://ctf.hackthebox.com/event/123
        )
        self._http = http

        super().__init__(
            session=CoreSessionHelper(self),
            attachments=CoreAttachmentService(self),  # Uses core attachment logic
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

    @property
    def _ctf_id(self) -> str:
        return self._platform_url.split("/")[-1]

    def _get_api_url(self, endpoint: str) -> str:  # This helper can remain
        # Note: This constructs an ABSOLUTE URL to the global HTB API,
        # not relative to self._platform_url.
        # This means HTB services will use self._client._http.get/post directly
        # with this absolute URL, NOT self._client.get/post which prepends platform_url.
        # This is because not all endpoints share the same base URL with the CTF id.
        path = endpoint.format()
        return urljoin("https://ctf.hackthebox.com/api/", path.lstrip("/"))
