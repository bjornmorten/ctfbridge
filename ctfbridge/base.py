from abc import ABC, abstractmethod
from typing import List

import requests

from .models import Challenge, SubmissionResult


class CTFPlatformClient(ABC):
    """Abstract base class for all CTF platform clients."""
    def __init__(self, base_url: str = ''):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    @abstractmethod
    def login(self, username: str = '', password: str = '', token: str = '') -> None:
        """Login using username and password."""
        pass

    @abstractmethod
    def get_challenges(self) -> List[Challenge]:
        """Retrieve a list of challenges."""
        pass

    @abstractmethod
    def get_challenge(self, challenge_id: int) -> Challenge:
        """Retrieve a specific challenge."""
        pass

    @abstractmethod
    def submit_flag(self, challenge_id: int, flag: str) -> SubmissionResult:
        """Submit a flag for a challenge."""
        pass

    def set_cookie(self, name: str, value: str, domain: str = None):
        """Manually set a cookie into the session."""
        if domain is None:
            domain = self._default_domain()
        self.session.cookies.set(name=name, value=value, domain=domain)

    def set_token(self, token: str) -> None:
        """Set a Bearer authentication token."""
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _default_domain(self) -> str:
        from urllib.parse import urlparse
        parsed = urlparse(self.base_url)
        return parsed.netloc