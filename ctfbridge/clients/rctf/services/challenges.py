from typing import List, Dict, Any

from ctfbridge.exceptions import ChallengeFetchError, SubmissionError
from ctfbridge.models.challenge import Attachment, Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.services import ChallengeService

class RCTFChallengeService(ChallengeService):
    """
    RCTF challenge service.
    """
    def __init__(self, client):
        super().__init__(client)

    def get_all(self) -> List[Challenge]:
        """Fetch all challenges."""
        url = f"{self.client.base_url}/api/v1/challs"
        response = self.client.session.get(url)
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

    def get_by_id(self, challenge_id: int) -> Challenge:
        """Fetch details for a specific challenge."""
        challenges = self.get_all()
        for chall in challenges:
            if chall.id == challenge_id:
                return chall
        raise ChallengeFetchError(f"Challenge with id {challenge_id} not found.")

    def submit(self, challenge_id: int, flag: str):
        """Submit a flag for a challenge."""
        url = f"{self.client.base_url}/api/v1/challs/{challenge_id}/submit"
        payload = {"flag": flag}

        resp = self.client.session.post(url, json=payload)

        try:
            result = resp.json()
        except Exception as e:
            raise SubmissionError("Invalid response format from server.")

        return SubmissionResult(
            correct=(resp.status_code == 200),
            message=result["message"]
        )

    def _get_profile(self) -> Dict[str, Any]:
        """Get user profile"""
        url = f"{self.client.base_url}/api/v1/users/me"
        response = self.client.session.get(url)
        response.raise_for_status()
        data = response.json()['data']
        return data