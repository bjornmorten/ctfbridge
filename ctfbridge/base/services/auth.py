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
            TokenAuthError: If token-based authentication fails.
            LoginError: If username/password login fails.
            MissingAuthMethodError: If no authentication method is provided.
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
