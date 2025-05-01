from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlparse

import requests

from .services.attachments import AttachmentService
from .services.auth import AuthService
from .services.challenges import ChallengeService
from .services.platform import PlatformService
from .services.scoreboard import ScoreboardService


class CTFPlatformClient(ABC):
    """
    Abstract base class for all CTF platform clients.

    Provides common interface methods and service properties for interacting
    with challenges, authentication, attachments, and scoreboard APIs.
    """

    def __init__(self, base_url: str):
        """
        Initialize the platform client.

        Args:
            base_url (str): The base URL of the CTF platform.
        """
        self.base_url = base_url
        self.session = requests.Session()

        self.auth: AuthService
        self.challenges: ChallengeService
        self.attachments: AttachmentService
        self.scoreboard: ScoreboardService
        self.platform: PlatformService

    def login(self, username: str = '', password: str = '', token: str = '') -> None:
        """
        Authenticate using the platform's authentication service.

        Args:
            username (str): Username to login with.
            password (str): Password to login with.
            token (str): Optional authentication token.
        """
        self.auth.login(username=username, password=password, token=token)

    def logout(self):
        """
        Log out of the current session.
        """
        self.auth.logout()

    def is_logged_in(self) -> bool:
        """
        Check if the current session is authenticated.

        Returns:
            bool: True if logged in, False otherwise.
        """
        return self.auth.is_logged_in()

    def save_session(self, path: str) -> None:
        """
        Save the current session to a file.

        Args:
            path (str): Path to the file to store session data.
        """
        self.auth.save_session(path)

    def load_session(self, path: str) -> None:
        """
        Load a session from a file.

        Args:
            path (str): Path to the session file.
        """
        self.auth.load_session(path)

    def set_token(self, token: str) -> None:
        """
        Set the session's Authorization header using a bearer token.

        Args:
            token (str): The authentication token.
        """
        self.session.headers["Authorization"] = f"Bearer {token}"

    def set_cookie(self, name: str, value: str, domain: Optional[str] = None) -> None:
        """
        Set a cookie for the session.

        Args:
            name (str): Cookie name.
            value (str): Cookie value.
            domain (Optional[str]): Domain to attach the cookie to. Defaults to the base URL's domain.
        """
        if domain is None:
            domain = self._default_domain()
        self.session.cookies.set(name=name, value=value, domain=domain)

    def set_headers(self, headers: dict) -> None:
        """
        Update session headers with custom values.

        Args:
            headers (dict): A dictionary of HTTP headers to set.
        """
        self.session.headers.update(headers)

    def _default_domain(self) -> str:
        """
        Get the domain from the base URL.

        Returns:
            str: Domain name extracted from the base URL.
        """
        return urlparse(self.base_url).netloc
