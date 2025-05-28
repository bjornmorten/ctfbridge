from .base import CTFBridgeError


class SessionError(CTFBridgeError):
    def __init__(self, path: str, operation: str, reason: str):
        super().__init__(f"Failed to {operation} session at {path}: {reason}")
        self.path = path
        self.operation = operation
        self.reason = reason
