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

    async def login(self, *, username: str = "", password: str = "", token: str = "") -> None:
        if token:
            await self._login_with_token(token)
        elif username and password:
            await self._login_with_credentials(username, password)
        else:
            logger.error("No authentication method provided.")
            raise MissingAuthMethodError()

    async def _login_with_token(self, token: str) -> None:
        try:
            logger.debug("Attempting token-based authentication.")
            await self._client.session.set_headers(
                {"Authorization": f"Token {token}", "Content-Type": "application/json"}
            )
            await self._client.get("me")
            logger.info("Token authentication successful.")
        except UnauthorizedError as e:
            logger.warning("Unauthorized token provided.")
            raise TokenAuthError("Unauthorized token") from e

    async def _login_with_credentials(self, username: str, password: str) -> None:
        try:
            logger.debug("Fetching login page for nonce.")
            resp = await self._client.get("login")
            nonce = self._extract_login_nonce(resp.text)
            if not nonce:
                logger.warning("Login nonce not found in login page.")
                raise LoginError(username)

            logger.debug("Posting credentials for user %s", username)
            resp = await self._client.post(
                "login",
                data={"name": username, "password": password, "nonce": nonce},
                follow_redirects=False,
            )

            if resp.status_code == 403 or "incorrect" in resp.text.lower():
                logger.warning("Incorrect credentials or login denied for user %s", username)
                raise LoginError(username)

            logger.info("Credential-based login successful for user %s", username)
        except Exception as e:
            logger.exception("Credential-based login failed")
            raise LoginError(username) from e

    @staticmethod
    def _extract_login_nonce(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.find("input", {"name": "nonce", "type": "hidden"})
        return tag.get("value", "") if tag and isinstance(tag, Tag) else ""

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        return [AuthMethod.CREDENTIALS, AuthMethod.TOKEN]
