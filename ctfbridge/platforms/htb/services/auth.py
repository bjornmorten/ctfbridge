import logging
from typing import List
from urllib.parse import parse_qs, unquote, urlparse

from bs4 import BeautifulSoup, Tag

from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import LoginError, MissingAuthMethodError, TokenAuthError
from ctfbridge.models.auth import AuthMethod

logger = logging.getLogger(__name__)


class HTBAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def login(
        self, *, username: str = "", password: str = "", token: str = ""
    ) -> None:
        if token:
            try:
                logger.debug("Attempting token-based authentication.")
                await self._client.session.set_token(token)
                resp = await self._client._http.get(
                    self._client._get_api_url(f"ctfs/{self._client._ctf_id}")
                )
                if resp.status_code != 200:
                    logger.warning(
                        "Token authentication failed with status %s", resp.status_code
                    )
                    raise TokenAuthError("Unauthorized token")
                logger.info("Token authentication successful.")
            except Exception as e:
                raise TokenAuthError(str(e)) from e

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        return [AuthMethod.TOKEN]
