from typing import List, Optional, Optional

from ctfbridge.models.challenge import Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.services import ChallengeService
from ctfbridge.exceptions import ChallengeFetchError

class DemoChallengeService(ChallengeService):
    """
    CTFd challenge service.
    """
    challenges = [
        Challenge(
            id=1,
            name="Basic Web Login",
            category="Web",
            value=100,
            description="Can you bypass the login page somehow?",
            solved=False
        ),
        Challenge(
            id=2,
            name="Buffer Overflow 101",
            category="Pwn",
            value=200,
            description="There's a vulnerable buffer in this binary. Can you smash it?",
            solved=False
        ),
        Challenge(
            id=3,
            name="Simple Crypto",
            category="Crypto",
            value=150,
            description="This message was encrypted with a simple cipher. Break it!",
            solved=False
        ),
        Challenge(
            id=4,
            name="Stego Secrets",
            category="Forensics",
            value=250,
            description="There's something hidden in this image file. Can you extract it?",
            solved=False
        ),
        Challenge(
            id=5,
            name="Intro to Reverse Engineering",
            category="Reversing",
            value=300,
            description="Decompile this binary and find the secret key.",
            solved=False
        ),
    ]    

    def __init__(self, client):
        super().__init__(client)

    def get_all(self) -> List[Challenge]:
        """Fetch all challenges."""
        return self.challenges

    def get_by_id(self, challenge_id: int) -> Optional[Challenge]:
        """Fetch details for a specific challenge."""
        for challenge in self.challenges:
            if challenge.id == challenge_id:
                return challenge
        
        raise ChallengeFetchError("Could not fetch challenge.")

    def submit(self, challenge_id: int, flag: str):
        """Submit a flag for a challenge."""
        if flag == "DEMO{flag}":
            return SubmissionResult(
                correct=True,
                message="Correct!"
            )
        else:
            return SubmissionResult(
                correct=False,
                message="Wrong!"
            )