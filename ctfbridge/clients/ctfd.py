import re
from typing import List
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup

from ..base import CTFPlatformClient
from ..exceptions import ChallengeFetchError, LoginError, SubmissionError
from ..models import Attachment, Challenge, ScoreboardEntry, SubmissionResult


class CTFdClient(CTFPlatformClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    @property
    def platform(self) -> str:
        return "CTFd"

    @property
    def auth_type(self) -> str:
        return "credentials"

    def login(self, username: str = '', password: str = '', token: str = '') -> None:
        """Login to CTFd platform."""
        # Get nonce
        resp = self.session.get(f"{self.base_url}/login")

        nonce = self._extract_login_nonce(resp.text)
        if not nonce:
            raise LoginError("Failed to extract CSRF token for login.")

        # Post login credentials
        resp = self.session.post(
            f"{self.base_url}/login",
            data={"name": username, "password": password, "nonce": nonce}
        )

        # Check if login succeeded
        if "incorrect" in resp.text.lower():
            raise LoginError("Incorrect username or password.")

    def get_challenges(self) -> List[Challenge]:
        """Fetch all challenges."""
        resp = self.session.get(f"{self.base_url}/api/v1/challenges")

        try:
            data = resp.json()["data"]
        except Exception:
            raise ChallengeFetchError("Invalid response format from server.")

        challenges = []
        for chal in data:
            challenges.append(
                self.get_challenge(chal["id"])
            )
        return challenges

    def get_challenge(self, challenge_id: int) -> Challenge:
        """Fetch details for a specific challenge."""
        resp = self.session.get(f"{self.base_url}/api/v1/challenges/{challenge_id}")

        try:
            chal = resp.json()["data"]
        except Exception:
            raise ChallengeFetchError("Invalid response format from server.")

        attachments = [
            Attachment(
                name=unquote(urlparse(url).path.split("/")[-1]),
                url=self._full_url(url)
            )
            for url in chal.get("files", [])
        ]

        return Challenge(
            id=chal["id"],
            name=chal["name"],
            category=chal["category"],
            value=chal["value"],
            description=chal.get("description", ""),
            attachments=attachments,
            solved=chal.get("solved_by_me", False)
        )


    def submit_flag(self, challenge_id: int, flag: str) -> SubmissionResult:
        """Submit a flag for a challenge."""
        resp = self.session.get(self.base_url)
        csrf_token = self._extract_csrf_nonce(resp.text)

        resp = self.session.post(
            f"{self.base_url}/api/v1/challenges/attempt",
            json={"challenge_id": challenge_id, "submission": flag},
            headers={"CSRF-Token": csrf_token}
        )        

        try:
            result = resp.json()["data"]
        except Exception as e:
            raise SubmissionError("Invalid response format from server.")

        return SubmissionResult(
            correct=(result["status"] == "correct"),
            message=result["message"]
        )

    def get_scoreboard(self, limit = 0) -> List[ScoreboardEntry]:
        resp = self.session.get(
            f"{self.base_url}/api/v1/scoreboard",
        )

        try:
            data = resp.json()["data"]
        except Exception:
            raise ChallengeFetchError("Invalid response format from server (scoreboard).")

        scoreboard = []
        for entry in data:
            scoreboard.append(
                ScoreboardEntry(
                    name=entry.get("name", "unknown"),
                    score=entry.get("score", 0),
                    rank=entry.get("pos", 0)
                )
            )
        
        if limit:
            return scoreboard[:limit]
        else:
            return scoreboard


    def _extract_login_nonce(self, html: str) -> str:
        """Extract the login nonce from the HTML login page."""
        soup = BeautifulSoup(html, "html.parser")
        nonce_input = soup.find("input", {"name": "nonce", "type": "hidden"})
        if nonce_input and nonce_input.has_attr("value"):
            return nonce_input["value"]
        return ""

    def _extract_csrf_nonce(self, html: str) -> str:
        """Extract the CSRF nonce from the HTML source."""
        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")
        for script in scripts:
            if script.string and "csrfNonce" in script.string:
                match = re.search(r"'csrfNonce':\s*\"([a-fA-F0-9]+)\"", script.string)
                if match:
                    return match.group(1)
        return ""

    def _full_url(self, path: str) -> str:
        """Convert a relative attachment path to a full URL."""
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
