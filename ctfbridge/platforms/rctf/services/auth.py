import logging
from typing import List
from urllib.parse import parse_qs, unquote, urlparse

from bs4 import BeautifulSoup, Tag

from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import LoginError, MissingAuthMethodError, TokenAuthError
from ctfbridge.models.auth import AuthMethod

logger = logging.getLogger(__name__)


class RCTFAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def login(self, *, username: str = "", password: str = "", token: str = "") -> None:
        base_url = self._client._platform_url
        http = self._client._http

        if token:
            try:
                # Normalise the incoming token: allow full invite URLs and
                # percent‑encoded strings.
                if token.startswith("http"):
                    token = self._extract_token_from_url(token)
                else:
                    token = unquote(token)

                logger.debug("Attempting rCTF team-token login.")
                resp = await http.post(f"{base_url}/api/v1/auth/login", json={"teamToken": token})

                if resp.status_code != 200:
                    logger.warning("Team token login failed with status %s", resp.status_code)
                    raise TokenAuthError("Unauthorized token")

                result = resp.json()
                if result.get("kind") != "goodLogin":
                    logger.error("Unexpected login response: %s", result)
                    raise TokenAuthError("Login failed: Unexpected server response.")

                auth_token = result["data"]["authToken"]
                await self._client.session.set_token(auth_token)
                logger.info("Team-token authentication successful.")
                return
            except Exception as e:
                raise TokenAuthError(str(e)) from e

    @staticmethod
    def _extract_token_from_url(url: str) -> str:
        """Extract team token from team invite URL."""
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        extracted_token_list = query_params.get("token")
        if not extracted_token_list:
            raise ValueError("Invalid token URL: no token parameter found.")
        token = extracted_token_list[0]
        return token

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        return [AuthMethod.TOKEN]
