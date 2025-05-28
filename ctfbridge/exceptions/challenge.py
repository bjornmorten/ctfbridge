from .base import CTFBridgeError


class ChallengeFetchError(CTFBridgeError):
    def __init__(self, reason: str):
        super().__init__(f"Failed to fetch challenges: {reason}")


class SubmissionError(CTFBridgeError):
    def __init__(self, challenge_id: str, flag: str, reason: str):
        super().__init__(f"Failed to submit flag to challenge '{challenge_id}': {reason}")
        self.challenge_id = challenge_id
        self.flag = flag
        self.reason = reason


class CTFInactiveError(CTFBridgeError):
    def __init__(self, reason: str = "The CTF is not currently active."):
        super().__init__(reason)
