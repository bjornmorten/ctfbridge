from typing import List, Optional

from ctfbridge.exceptions import ChallengeFetchError
from ctfbridge.models.challenge import Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.services import ChallengeService


class DemoChallengeService(ChallengeService):
    """
    Demo challenge service.
    """
    def __init__(self, client):
        super().__init__(client)

    def get_all(self) -> List[Challenge]:
        """Fetch all challenges."""
        return self.client.demo_platform.get_all_challenges()

    def get_by_id(self, challenge_id: int) -> Optional[Challenge]:
        """Fetch details for a specific challenge."""
        try: 
            return self.client.demo_platform.get_challenge_by_id(challenge_id)
        except ValueError:
            raise ChallengeFetchError("Could not fetch challenge.")

    def submit(self, challenge_id: int, flag: str):
        """Submit a flag for a challenge."""
        return self.client.demo_platform.submit_flag(challenge_id, flag)
