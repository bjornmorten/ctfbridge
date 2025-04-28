from typing import Any, Dict, List
from urllib.parse import parse_qs, unquote, urlparse

from ..base import CTFPlatformClient
from ..models import Challenge, SubmissionResult


class RCTFClient(CTFPlatformClient):
    """Concrete client implementation for rCTF platform."""
    
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
        solved_ids = [chal['id'] for chal in solves]

        challenges = []
        for chall in challs_data:
            print(chall)
            challenges.append(
                Challenge(
                    id=chall["id"],
                    name=chall["name"],
                    category=chall["category"],
                    value=chall["points"],
                    description=chall["description"],
                    attachments=[file['url'] for file in chall["files"]],
                    solved=(chall["id"] in solved_ids),
                    extra={
                        'author': chall.get('author')
                    }
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
        raise NotImplementedError

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