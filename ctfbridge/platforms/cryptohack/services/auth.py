import logging
from typing import List

from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import LoginError
from ctfbridge.models.auth import AuthMethod
from ctfbridge.platforms.cryptohack.utils.csrf import get_csrf_token

logger = logging.getLogger(__name__)


class CryptoHackAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def _login_with_credentials(self, username: str, password: str) -> None:
        try:
            csrf_token = await get_csrf_token(self._client._http)

            logger.debug("Posting credentials for user %s", username)
            resp = await self._client.post(
                "/login/",
                data={"username": username, "password": password, "_csrf_token": csrf_token},
                follow_redirects=True,
            )

            if "Login successful" not in resp.text:
                logger.debug("Incorrect credentials or login denied for user %s", username)
                raise LoginError(username)

            logger.info("Credential-based login successful for user %s", username)

        except Exception as e:
            logger.debug("Credential-based login failed")
            raise LoginError(username) from e

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        return [AuthMethod.CREDENTIALS]
