import os
from abc import ABC, abstractmethod
from typing import List, Optional
from urllib.parse import urlparse

import requests

from .models import Attachment, Challenge, ScoreboardEntry, SubmissionResult


class CTFPlatformClient(ABC):
    """Abstract base class for all CTF platform clients."""
    def __init__(self, base_url: str = ''):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    @property
    @abstractmethod
    def platform(self) -> str:
        """Return the name of the platform (e.g., 'CTFd', 'rCTF')."""
        pass

    @property
    @abstractmethod
    def auth_type(self) -> str:
        """Return the authentication type of the platform (e.g., 'credentials', 'token')."""
        pass

    @abstractmethod
    def login(self, username: str = '', password: str = '', token: str = '') -> None:
        """Login using username and password or token."""
        pass

    def logout(self) -> None:
        """Log out and clean up the session."""
        self.session.cookies.clear()
        self.session.headers.pop("Authorization", None)

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

    def get_scoreboard(self, limit: int = 0) -> List[ScoreboardEntry]:
        """Get the scoreboard."""
        raise NotImplementedError("Scoreboard not supported.")

    def set_cookie(self, name: str, value: str, domain: Optional[str] = None):
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

    def download_attachment(
        self,
        attachment: Attachment,
        save_dir: str,
        filename: Optional[str] = None
    ) -> str:
        """Download an attachment file and save it locally."""
        os.makedirs(save_dir, exist_ok=True)

        url = attachment.url
        final_filename = filename if filename is not None else attachment.name
        save_path = os.path.join(save_dir, final_filename)
        
        # Only use auth session if attachment is on the same domain as the CTF.
        if urlparse(self.base_url).netloc == urlparse(url).netloc:
            resp = self.session.get(url, stream=True)
        else:
            resp = requests.get(url, stream=True)

        if resp.status_code != 200:
            raise Exception(f"Failed to download attachment: {url} (status {resp.status_code})")

        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1048576):
                if chunk:
                    f.write(chunk)

        return save_path
