import logging
from abc import abstractmethod
from typing import List

from ctfbridge.base.services.auth import AuthService
from ctfbridge.exceptions import InvalidAuthMethodError, MissingAuthMethodError
from ctfbridge.models.auth import AuthMethod

logger = logging.getLogger(__name__)


class CoreAuthService(AuthService):
    def __init__(self, client):
        self._client = client

    async def login(self, *, username: str = "", password: str = "", token: str = "") -> None:
        supported_methods = await self.get_supported_auth_methods()

        if token:
            if AuthMethod.TOKEN not in supported_methods:
                logger.error("Token-based authentication is not supported.")
                raise InvalidAuthMethodError("Token authentication not supported.")
            await self._login_with_token(token)

        elif username and password:
            if AuthMethod.CREDENTIALS not in supported_methods:
                logger.error("Credential-based authentication is not supported.")
                raise InvalidAuthMethodError("Username/password authentication not supported.")
            await self._login_with_credentials(username, password)

        else:
            logger.error("No authentication method provided.")
            raise InvalidAuthMethodError("No valid authentication method provided.")

    async def logout(self):
        self._client.http.cookies.clear()
        self._client.http.session.headers.pop("Authorization", None)

    @abstractmethod
    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        pass

    async def _login_with_token(self, token: str) -> None:
        raise NotImplementedError("Token authentication not implemented for this platform.")

    async def _login_with_credentials(self, username: str, password: str) -> None:
        raise NotImplementedError("Credential authentication not implemented for this platform.")
