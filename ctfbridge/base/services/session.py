from abc import ABC
from typing import Dict


class SessionHelper(ABC):
    """
    HTTP session management.
    """

    async def set_token(self, token: str) -> None:
        """
        Set a bearer token in the session headers.

        Args:
            token: The bearer token to use for authentication.
        """
        raise NotImplementedError

    async def set_headers(self, headers: Dict[str, str]) -> None:
        """
        Update session headers with custom key-value pairs.

        Args:
            headers: A dictionary of headers to add or update.
        """
        raise NotImplementedError

    async def set_cookie(
        self, name: str, value: str, domain: str | None = None
    ) -> None:
        """
        Set a cookie in the session.

        Args:
            name: Name of the cookie.
            value: Value of the cookie.
            domain: The domain for which the cookie is valid.
        """
        raise NotImplementedError

    async def save(self, path: str) -> None:
        """
        Save the session's current state, including cookies and headers, to a file.

        Args:
            path: Path to the file where session state should be saved.

        Raises:
            SessionError: If saving the session fails (e.g., due to file I/O issues).
        """
        raise NotImplementedError

    async def load(self, path: str) -> None:
        """
        Load the session state (cookies and headers) from a file.

        Args:
            path: Path to the file from which to load the session state.

        Raises:
            SessionError: If loading the session fails (e.g., file not found or corrupt).
        """
        raise NotImplementedError
