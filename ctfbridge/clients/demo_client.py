from typing import List
from ..base import CTFPlatformClient
from ..models import Challenge, SubmissionResult

class DemoClient(CTFPlatformClient):
    """Demo CTF client for testing purposes."""

    def __init__(self, base_url: str = ''):
        super().__init__(base_url)

        self.logged_in = False
        self.challenges = [
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

    def login(self, username: str, password: str) -> None:
        if username == "demo" and password == "demo":
            self.logged_in = True
        else:
            raise ValueError("Incorrect credentials for demo.")

    def get_challenges(self) -> List[Challenge]:
        if not self.logged_in:
            raise ValueError("Must login first.")
        return self.challenges

    def get_challenge(self, challenge_id: int) -> Challenge:
        if not self.logged_in:
            raise ValueError("Must login first.")
        for chal in self.challenges:
            if chal.id == challenge_id:
                return chal
        raise ValueError("Challenge not found.")

    def submit_flag(self, challenge_id: int, flag: str) -> SubmissionResult:
        if not self.logged_in:
            raise ValueError("Must login first.")
        if flag == "flag{demo}":
            return SubmissionResult(correct=True, message="Correct demo flag!")
        return SubmissionResult(correct=False, message="Incorrect flag.")
