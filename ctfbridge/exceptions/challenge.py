from .base import CTFBridgeError


class ChallengeFetchError(CTFBridgeError):
    def __init__(self, reason: str):
        super().__init__(f"Failed to fetch challenges: {reason}")


class ChallengeNotFoundError(CTFBridgeError):
    def __init__(self, challenge_id: str):
        super().__init__(f"Challenge with ID '{challenge_id}' not found.")
        self.challenge_id = challenge_id


class ChallengesUnavailableError(CTFBridgeError):
    """Raised when challenges are not accessible, possibly because the CTF hasn't started or has ended."""

    def __init__(
        self,
        message: str = "Challenges are not available. The CTF may not have started or may have ended.",
    ):
        super().__init__(message)


class SubmissionError(CTFBridgeError):
    def __init__(self, challenge_id: str, flag: str, reason: str):
        super().__init__(f"Failed to submit flag to challenge '{challenge_id}': {reason}")
        self.challenge_id = challenge_id
        self.flag = flag
        self.reason = reason


class CTFInactiveError(CTFBridgeError):
    def __init__(self, reason: str = "The CTF is not currently active."):
        super().__init__(reason)
