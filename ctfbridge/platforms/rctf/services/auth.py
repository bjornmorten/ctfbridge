import logging
from typing import List
from urllib.parse import parse_qs, unquote, urlparse

import httpx
from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import MissingAuthMethodError, TokenAuthError
from ctfbridge.models.auth import AuthMethod
from ctfbridge.platforms.rctf.http.endpoints import Endpoints

logger = logging.getLogger(__name__)


class RCTFAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def login(self, *, username: str = "", password: str = "", token: str = "") -> None:
        """
        Login using a team token (rCTF doesn't use username/password auth).
        """
        if not token:
            raise MissingAuthMethodError("rCTF only supports token-based login.")

        token = self._normalize_token(token)
        logger.debug("Attempting rCTF token login with token: [REDACTED]")

        try:
            response = await self._client.post(
                Endpoints.Auth.LOGIN,
                json={"teamToken": token},
            )

            if response.status_code != 200:
                logger.debug(f"Token login failed with HTTP {response.status_code}")
                raise TokenAuthError("Invalid token or login failed.")

            result = response.json()
            if result.get("kind") != "goodLogin":
                logger.error(f"Unexpected login response: {result}")
                raise TokenAuthError("Unexpected server response during login.")

            auth_token = result["data"].get("authToken")
            if not auth_token:
                raise TokenAuthError("No auth token returned by server.")

            await self._client.session.set_token(auth_token)
            logger.info("rCTF token login successful.")
        except TokenAuthError:
            raise
        except (httpx.HTTPError, ValueError) as e:
            logger.exception("Token login failed due to HTTP or parsing error.")
            raise TokenAuthError(f"Login failed: {str(e)}") from e
        except Exception as e:
            logger.exception("Unexpected error during token login.")
            raise TokenAuthError(f"Unexpected login error: {str(e)}") from e

    @staticmethod
    def _normalize_token(token: str) -> str:
        """
        Normalize a token input, extracting it if it's an invite URL.
        """
        if token.startswith("http"):
            parsed = urlparse(token)
            query_params = parse_qs(parsed.query)
            token_list = query_params.get("token")
            if not token_list:
                raise ValueError("Token URL does not contain a 'token' parameter.")
            return token_list[0]
        return unquote(token)

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        return [AuthMethod.TOKEN]
