from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.models.auth import AuthMethod
from ctfbridge.exceptions import LoginError, TokenAuthError, MissingAuthMethodError
from typing import List
from bs4 import BeautifulSoup, Tag
import logging

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
                await self._client.session.set_token(token)
                resp = await http.get(f"{base_url}/api/v1/users/me")
                if resp.status_code != 200:
                    logger.warning(
                        "Token authentication failed with status %s", resp.status_code
                    )
                    raise TokenAuthError("Unauthorized token")
                logger.info("Token authentication successful.")
            except Exception as e:
                raise TokenAuthError(str(e)) from e

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
