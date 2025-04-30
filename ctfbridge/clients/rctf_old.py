from typing import Any, Dict, List
from urllib.parse import parse_qs, unquote, urlparse

from ..base import CTFPlatformClient
from ..exceptions import SubmissionError
from ..models import Attachment, Challenge, ScoreboardEntry, SubmissionResult


class RCTFClient(CTFPlatformClient):
    """Concrete client implementation for rCTF platform."""

    @property
    def platform(self) -> str:
        return "rCTF"

    @property
    def auth_type(self) -> str:
        return "token"
    
    def login(self, username: str = '', password: str = '', token: str = '') -> None:
        """Login to rCTF."""
        if not token:
            raise ValueError("You must provide a team token for rCTF login.")

        if token.startswith("http"):
            token = self._extract_token_from_url(token)
        else:
            token = unquote(token)

        url = f"{self.base_url}/api/v1/auth/login"
        payload = {"teamToken": token}

        response = self.session.post(url, json=payload)
        response.raise_for_status()

        result = response.json()
        if result["kind"] != "goodLogin":
            raise ValueError("Login failed: Unexpected server response.")

        auth_token = result["data"]["authToken"]
        self.set_token(auth_token)

    def get_challenges(self) -> List[Challenge]:
        """Retrieve a list of challenges."""
        url = f"{self.base_url}/api/v1/challs"
        response = self.session.get(url)
        response.raise_for_status()
        challs_data = response.json()["data"]

        solves = self._get_profile()['solves']
        solved_ids = [chal["id"] for chal in solves]

        challenges = []
        for chall in challs_data:
            challenges.append(
                Challenge(
                    id=chall["id"],
                    name=chall["name"],
                    category=chall["category"],
                    value=chall["points"],
                    description=chall["description"],
                    attachments=[
                        Attachment(name=file["name"], url=file["url"])
                        for file in chall["files"]
                    ],
                    solved=(chall["id"] in solved_ids),
                    author=chall.get('author')
                )
            )
        return challenges

    def get_challenge(self, challenge_id: int) -> Challenge:
        """Retrieve a specific challenge."""
        challenges = self.get_challenges()
        for chall in challenges:
            if chall.id == challenge_id:
                return chall
        raise ValueError(f"Challenge with id {challenge_id} not found.")
    
    def submit_flag(self, challenge_id: int, flag: str) -> SubmissionResult:
        """Submit a flag for a challenge."""
        url = f"{self.base_url}/api/v1/challs/{challenge_id}/submit"
        payload = {"flag": flag}

        resp = self.session.post(url, json=payload)

        try:
            result = resp.json()
        except Exception as e:
            raise SubmissionError("Invalid response format from server.")

        return SubmissionResult(
            correct=(result["status"] == 200),
            message=result["message"]
        )

    def get_scoreboard(self, limit: int = 0):
        resp = self.session.get(f"{self.base_url}/api/v1/leaderboard/now?limit=0&offset=100")
        total = resp.json()["data"]["total"]

        if limit:
            limit = min(limit, total)
        else:
            limit = total

        scoreboard = []
        for offset in range(0, limit, 100):
            curr_limit = min(100, limit - offset)
            resp = self.session.get(f"{self.base_url}/api/v1/leaderboard/now?limit={curr_limit}&offset={offset}")

            partial_scoreboard = resp.json()["data"]["leaderboard"]
            for i, entry in enumerate(partial_scoreboard):
                scoreboard.append(ScoreboardEntry(
                    name=entry["name"],
                    score=entry["score"],
                    rank=offset + i + 1
                ))

        return scoreboard

    def _get_profile(self) -> Dict[str, Any]:
        """Get user profile"""
        url = f"{self.base_url}/api/v1/users/me"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()['data']
        return data

    def _extract_token_from_url(self, url: str) -> str:
        """Extract team token from team invite URL."""
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        extracted_token_list = query_params.get("token")
        if not extracted_token_list:
            raise ValueError("Invalid token URL: no token parameter found.")
        token = extracted_token_list[0]
        return token
