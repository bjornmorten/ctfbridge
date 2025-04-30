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
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

        self.auth: AuthService
        self.challenges: ChallengeService
        self.attachments: AttachmentService
        self.scoreboard: ScoreboardService
        self.platform: PlatformService

    def login(self, username: str = '', password: str = '', token: str = '') -> None:
        """Authenticate using the platform's auth service."""
        self.auth.login(username=username, password=password, token=token)

    def logout(self):
        self.auth.logout()

    def is_logged_in(self) -> bool:
        """Return whether the session is currently authenticated."""
        return self.auth.is_logged_in()

    def save_session(self, path: str) -> None:
        """Save the session to a file."""
        self.auth.save_session(path)

    def load_session(self, path: str) -> None:
        """Load session from a file."""
        self.auth.load_session(path)

    def set_token(self, token: str) -> None:
        self.session.headers["Authorization"] = f"Bearer {token}"

    def set_cookie(self, name: str, value: str, domain: Optional[str] = None) -> None:
        if domain is None:
            domain = self._default_domain()
        self.session.cookies.set(name=name, value=value, domain=domain)

    def set_headers(self, headers: dict) -> None:
        self.session.headers.update(headers)

    def _default_domain(self) -> str:
        return urlparse(self.base_url).netloc
