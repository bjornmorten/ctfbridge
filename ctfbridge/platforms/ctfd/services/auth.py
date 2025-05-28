import logging
from typing import List

from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import LoginError, TokenAuthError, UnauthorizedError
from ctfbridge.models.auth import AuthMethod
from ctfbridge.platforms.ctfd.utils import extract_csrf_nonce

logger = logging.getLogger(__name__)


class CTFdAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def _login_with_token(self, token: str) -> None:
        logger.debug("Setting token-based authentication.")
        await self._client.session.set_headers(
            {"Authorization": f"Token {token}", "Content-Type": "application/json"}
        )

    async def _login_with_credentials(self, username: str, password: str) -> None:
        try:
            resp = await self._client.get("login")
            nonce = extract_csrf_nonce(resp.text)
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

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        return [AuthMethod.CREDENTIALS, AuthMethod.TOKEN]
