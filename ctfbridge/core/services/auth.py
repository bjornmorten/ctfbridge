import logging
from abc import abstractmethod
from typing import List

from ctfbridge.base.services.auth import AuthService
from ctfbridge.exceptions import InvalidAuthMethodError, MissingAuthMethodError
from ctfbridge.models.auth import AuthMethod

logger = logging.getLogger(__name__)


class CoreAuthService(AuthService):
    """
    Core implementation of the authentication service.
    Provides common authentication flow and error handling.
    """

    def __init__(self, client):
        """
        Initialize the auth service.

        Args:
            client: The CTF client instance
        """
        self._client = client
        self.active_auth_method: str | AuthMethod = None

    async def login(self, *, username: str = "", password: str = "", token: str = "") -> None:
        supported_methods = await self.get_supported_auth_methods()

        if token:
            if AuthMethod.TOKEN not in supported_methods:
                logger.error("Token-based authentication is not supported.")
                raise InvalidAuthMethodError("Token authentication not supported.")
            await self._login_with_token(token)
            self.active_auth_method = AuthMethod.TOKEN

        elif username and password:
            if AuthMethod.CREDENTIALS not in supported_methods:
                logger.error("Credential-based authentication is not supported.")
                raise InvalidAuthMethodError("Username/password authentication not supported.")
            await self._login_with_credentials(username, password)
            self.active_auth_method = AuthMethod.CREDENTIALS

        else:
            logger.error("No authentication method provided.")
            raise InvalidAuthMethodError("No valid authentication method provided.")

    async def logout(self):
        self._client._http.cookies.clear()
        self._client._http.headers.pop("Authorization", None)
        self.active_auth_method = None

    @abstractmethod
    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        pass

    async def _login_with_token(self, token: str) -> None:
        """
        Authenticate using a token.
        Must be implemented by platform-specific services that support token auth.

        Args:
            token: The authentication token

        Raises:
            NotImplementedError: If token auth is not implemented
        """
        raise NotImplementedError("Token authentication not implemented for this platform.")

    async def _login_with_credentials(self, username: str, password: str) -> None:
        """
        Authenticate using username and password.
        Must be implemented by platform-specific services that support credential auth.

        Args:
            username: The username
            password: The password

        Raises:
            NotImplementedError: If credential auth is not implemented
        """
        raise NotImplementedError("Credential authentication not implemented for this platform.")
