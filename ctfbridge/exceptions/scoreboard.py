from .base import CTFBridgeError


class ScoreboardFetchError(CTFBridgeError):
    def __init__(self, reason: str):
        super().__init__(f"Failed to fetch scoreboard: {reason}")
