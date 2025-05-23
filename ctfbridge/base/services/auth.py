from abc import ABC
from typing import List

from ctfbridge.models.auth import AuthMethod


class AuthService(ABC):
    """
    Authentication service.
    """

    async def login(
        self, *, username: str = "", password: str = "", token: str = ""
    ) -> None:
        """
        Authenticate using the platform's authentication service.

        Args:
            username: Username to login with.
            password: Password to login with.
            token: Optional authentication token.

        Raises:
            TokenAuthError: If token authentication fails.
            LoginError: If username/password authentication fails.
            MissingAuthMethodError: If no auth method is provided.
            UnauthorizedError: If credentials are invalid.
            ServiceUnavailableError: If auth endpoint is unavailable.
        """
        raise NotImplementedError

    async def logout(self):
        """
        Log out of the current session.
        """
        raise NotImplementedError

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        """
        Get supported authentication methods.
        """
        raise NotImplementedError
