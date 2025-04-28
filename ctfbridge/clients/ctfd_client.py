from bs4 import BeautifulSoup
from typing import List
from ..base import CTFPlatformClient
from ..models import Challenge, SubmissionResult
from ..exceptions import LoginError, ChallengeFetchError, SubmissionError

class CTFdClient(CTFPlatformClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def login(self, username: str, password: str) -> None:
        """Login to CTFd platform."""
        # Get nonce
        resp = self.session.get(f"{self.base_url}/login")

        nonce = self._extract_nonce(resp.text)
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

        return Challenge(
            id=chal["id"],
            name=chal["name"],
            category=chal["category"],
            value=chal["value"],
            description=chal.get("description", ""),
            attachments=[self._full_url(f) for f in chal.get("files", [])],
            solved=chal.get("solved_by_me", False)
        )

    def submit_flag(self, challenge_id: int, flag: str) -> SubmissionResult:
        """Submit a flag for a challenge."""
        resp = self.session.post(
            f"{self.base_url}/api/v1/challenges/attempt",
            json={"challenge_id": challenge_id, "submission": flag}
        )

        try:
            result = resp.json()["data"]
        except Exception:
            raise SubmissionError("Invalid response format from server.")

        return SubmissionResult(
            correct=(result["status"] == "correct"),
            message=result["message"]
        )

    def _extract_nonce(self, html: str) -> str:
        """Extract the login nonce from the HTML login page."""
        soup = BeautifulSoup(html, "html.parser")
        nonce_input = soup.find("input", {"name": "nonce", "type": "hidden"})
        if nonce_input and nonce_input.has_attr("value"):
            return nonce_input["value"]
        return ""

    def _full_url(self, path: str) -> str:
        """Convert a relative attachment path to a full URL."""
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
