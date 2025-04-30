from typing import List, Optional
from urllib.parse import unquote, urlparse

from ctfbridge.exceptions import ChallengeFetchError, SubmissionError
from ctfbridge.models.challenge import Attachment, Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.services import ChallengeService

from ..utils import extract_csrf_nonce


class CTFdChallengeService(ChallengeService):
    """
    CTFd challenge service.
    """
    def __init__(self, client):
        super().__init__(client)

    def get_all(self) -> List[Challenge]:
        """Fetch all challenges."""
        resp = self.client.session.get(f"{self.client.base_url}/api/v1/challenges")

        try:
            data = resp.json()["data"]
        except Exception:
            raise ChallengeFetchError("Invalid response format from server.")

        challenges = []
        for chal in data:
            chal_detailed = self.get_by_id(chal["id"])
            if chal_detailed:
                challenges.append(
                    chal_detailed
                )
        return challenges

    def get_by_id(self, challenge_id: int) -> Challenge:
        """Fetch details for a specific challenge."""
        resp = self.client.session.get(f"{self.client.base_url}/api/v1/challenges/{challenge_id}")
        try:
            chal = resp.json()["data"]
        except Exception:
            raise ChallengeFetchError("Invalid response format from server.")

        attachments = [
            Attachment(
                name=unquote(urlparse(url).path.split("/")[-1]),
                url=(
                    url
                    if url.startswith(("http://", "https://"))
                    else self.client.base_url + "/" + url
                )
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

    def submit(self, challenge_id: int, flag: str):
        """Submit a flag for a challenge."""
        resp = self.client.session.get(self.client.base_url)
        csrf_token = extract_csrf_nonce(resp.text)

        resp = self.client.session.post(
            f"{self.client.base_url}/api/v1/challenges/attempt",
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
