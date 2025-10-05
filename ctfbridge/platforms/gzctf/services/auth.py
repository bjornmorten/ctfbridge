import logging

from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import LoginError
from ctfbridge.models.auth import AuthMethod
from ctfbridge.platforms.gzctf.http.endpoints import Endpoints

logger = logging.getLogger(__name__)


class GZCTFAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def _login_with_token(self, token: str) -> None:
        logger.debug("Setting token-based authentication.")
        await self._client.session.set_cookie("GZCTF_Token", token)

    async def _login_with_credentials(self, username: str, password: str) -> None:
        try:
            login_url = Endpoints.Auth.LOGIN

            logger.debug("Posting credentials for user %s", username)
            resp = await self._client.post(
                login_url, json={"userName": username, "password": password}
            )

            if resp.status_code == 401:
                logger.debug("Incorrect credentials or login denied for user %s", username)
                raise LoginError(username)

            if resp.status_code != 200:
                logger.debug("Unexpected error on login for", username)
                raise LoginError(username)

            logger.info("Credential-based login successful for user %s", username)

        except Exception as e:
            logger.debug("Credential-based login failed")
            raise LoginError(username) from e

    async def get_supported_auth_methods(self) -> list[AuthMethod]:
        return [AuthMethod.CREDENTIALS, AuthMethod.TOKEN]
