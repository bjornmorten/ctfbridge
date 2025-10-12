import logging

from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import LoginError
from ctfbridge.models.auth import AuthMethod

logger = logging.getLogger(__name__)


class PwnableKRAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def _login_with_credentials(self, username: str, password: str) -> None:
        try:
            logger.debug("Posting credentials for user %s", username)
            resp = await self._client.post(
                "/lib.php",
                params={"cmd": "login"},
                data={
                    "username": username,
                    "password": password,
                },
            )

            if "Login Ok" not in resp.text:
                logger.debug("Incorrect credentials or login denied for user %s", username)
                raise LoginError(username)

            logger.info("Credential-based login successful for user %s", username)

        except Exception as e:
            logger.debug("Credential-based login failed")
            raise LoginError(username) from e

    async def get_supported_auth_methods(self) -> list[AuthMethod]:
        return [AuthMethod.CREDENTIALS]
