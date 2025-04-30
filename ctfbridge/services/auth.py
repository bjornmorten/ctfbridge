import json
import os
from abc import ABC, abstractmethod


class AuthService(ABC):
    """
    Base authentication service.
    """

    def __init__(self, client):
        self.client = client

    @abstractmethod
    def login(self, username: str = '', password: str = '', token: str = '') -> None:
        """Authenticate and populate the session."""
        pass

    def logout(self):
        """Clear session cookies and headers."""
        self.client.session.cookies.clear()
        self.client.session.headers.pop("Authorization", None)

    def is_logged_in(self) -> bool:
        """Basic check for cookies or token. Platforms can override for API-based check."""
        return bool(self.client.session.cookies or "Authorization" in self.client.session.headers)

    def save_session(self, path: str) -> None:
        """Serialize cookies and headers to disk."""
        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = {
            "cookies": self.client.session.cookies.get_dict(),
            "headers": dict(self.client.session.headers)
        }

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def load_session(self, path: str) -> None:
        """Deserialize cookies and headers from disk."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Session file not found: {path}")

        with open(path, "r") as f:
            data = json.load(f)
            self.client.session.cookies.update(data.get("cookies", {}))
            self.client.session.headers.update(data.get("headers", {}))
