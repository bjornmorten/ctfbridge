import logging
from typing import List

from bs4 import BeautifulSoup, Tag

from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import (
    LoginError,
    MissingAuthMethodError,
    TokenAuthError,
    UnauthorizedError,
)
from ctfbridge.models.auth import AuthMethod

logger = logging.getLogger(__name__)


class CTFdAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def login(
        self, *, username: str = "", password: str = "", token: str = ""
    ) -> None:
        base_url = self._client._platform_url
        http = self._client._http

        if token:
            try:
                logger.debug("Attempting token-based authentication.")
                await self._client.session.set_headers(
                    {"Authorization": f"Token {token}"}
                )
                resp = await http.get(
                    f"{base_url}/api/v1/users/me",
                    headers={"Content-Type": "application/json"},
                )
                logger.info("Token authentication successful.")
            except UnauthorizedError as e:
                raise TokenAuthError("Unauthorized token") from e

        elif username and password:
            try:
                logger.debug("Fetching login page for nonce.")
                resp = await http.get(f"{base_url}/login")
                nonce = self._extract_login_nonce(resp.text)
                logger.debug("Extracted nonce: %s", nonce)
                if not nonce:
                    raise LoginError(username)

                logger.debug("Posting credentials for user %s", username)
                resp = await http.post(
                    f"{base_url}/login",
                    data={"name": username, "password": password, "nonce": nonce},
                )

                if "incorrect" in resp.text.lower():
                    logger.warning("Incorrect credentials for user %s", username)
                    raise LoginError(username)

                logger.info("Credential-based login successful for user %s", username)
            except Exception as e:
                raise LoginError(username) from e

        else:
            logger.error("No authentication method provided.")
            raise MissingAuthMethodError()

    @staticmethod
    def _extract_login_nonce(html: str) -> str | List[str]:
        """Extract CSRF nonce from login page HTML."""
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.find("input", {"name": "nonce", "type": "hidden"})
        return tag.get("value", "") if tag and isinstance(tag, Tag) else ""

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        return [AuthMethod.CREDENTIALS, AuthMethod.TOKEN]
