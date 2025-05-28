from .base import CTFBridgeError


class LoginError(CTFBridgeError):
    def __init__(self, username: str):
        super().__init__(f"Login failed for user '{username}'")
        self.username = username


class TokenAuthError(CTFBridgeError):
    def __init__(self, reason: str = ""):
        message = "Login failed using API token"
        if reason:
            message += f": {reason}"
        super().__init__(message)


class MissingAuthMethodError(CTFBridgeError):
    def __init__(self):
        super().__init__("No authentication method provided (username/password or API token)")


class InvalidAuthMethodError(CTFBridgeError):
    def __init__(self, message):
        super().__init__(message)


class SessionExpiredError(CTFBridgeError):
    def __init__(self):
        super().__init__("Session has expired or is invalid. Please re-authenticate.")
