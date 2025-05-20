"""
Defines the structured exception hierarchy for CTFBridge.
All custom errors inherit from CTFBridgeError.
"""

# ──────────────────────────────
# Base class
# ──────────────────────────────


class CTFBridgeError(Exception):
    """
    Base class for all CTFBridge errors.

    Subclasses should format their message in __init__ and pass it to super().
    """

    def __str__(self):
        return self.args[0] if self.args else self.__class__.__name__


# ──────────────────────────────
# 🌐 General HTTP/API errors
# ──────────────────────────────


class APIError(CTFBridgeError):
    """Base class for all HTTP API-related errors."""

    def __init__(self, message: str, *, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class BadRequestError(APIError):
    """400 Bad Request."""


class UnauthorizedError(APIError):
    """401 Unauthorized."""


class ForbiddenError(APIError):
    """403 Forbidden."""


class NotFoundError(APIError):
    """404 Not Found."""


class ConflictError(APIError):
    """409 Conflict."""


class ValidationError(APIError):
    """422 Unprocessable Entity."""


class ServerError(APIError):
    """5xx Server error."""


class ServiceUnavailableError(APIError):
    """503 Service unavailable."""


# ──────────────────────────────
# 🔐 Authentication-related errors
# ──────────────────────────────


class LoginError(CTFBridgeError):
    """Raised when username/password login fails."""

    def __init__(self, username: str):
        super().__init__(f"Login failed for user '{username}'")
        self.username = username


class TokenAuthError(CTFBridgeError):
    """Raised when API token authentication fails."""

    def __init__(self, reason: str = ""):
        message = "Login failed using API token"
        if reason:
            message += f": {reason}"
        super().__init__(message)
        self.reason = reason


class MissingAuthMethodError(CTFBridgeError):
    """Raised when no authentication method is provided."""

    def __init__(self):
        super().__init__(
            "No authentication method provided (username/password or API token)"
        )


class SessionExpiredError(CTFBridgeError):
    """Raised when the session is invalid or has expired."""

    def __init__(self):
        super().__init__("Session has expired or is invalid. Please re-authenticate.")


class RateLimitError(CTFBridgeError):
    """Raised when the server enforces rate limiting (HTTP 429)."""

    def __init__(self, retry_after: int | None = None):
        msg = "Rate limit exceeded."
        if retry_after is not None:
            msg += f" Retry after {retry_after} seconds."
        super().__init__(msg)
        self.retry_after = retry_after


# ──────────────────────────────
# 🎯 Scoreboard-related errors
# ──────────────────────────────


class ScoreboardFetchError(CTFBridgeError):
    """Raised when fetching scoreboard fails."""

    def __init__(self, reason: str):
        super().__init__(f"Failed to fetch scoreboard: {reason}")
        self.reason = reason


# ──────────────────────────────
# 🎯 Challenge-related errors
# ──────────────────────────────


class ChallengeFetchError(CTFBridgeError):
    """Raised when fetching challenges fails."""

    def __init__(self, reason: str):
        super().__init__(f"Failed to fetch challenges: {reason}")
        self.reason = reason


class SubmissionError(CTFBridgeError):
    """Raised when submitting a flag fails."""

    def __init__(self, challenge_id: str, flag: str, reason: str):
        super().__init__(
            f"Failed to submit flag to challenge '{challenge_id}': {reason}"
        )
        self.challenge_id = challenge_id
        self.flag = flag
        self.reason = reason


# ──────────────────────────────
# 🌐 Session related errors
# ──────────────────────────────


class SessionError(CTFBridgeError):
    """Raised when session state cannot be saved or loaded."""

    def __init__(self, path: str, operation: str, reason: str):
        super().__init__(f"Failed to {operation} session at {path}: {reason}")
        self.path = path
        self.operation = operation
        self.reason = reason


# ──────────────────────────────
# 📎 Attachment-related errors
# ──────────────────────────────


class AttachmentDownloadError(CTFBridgeError):
    """Raised when downloading an attachment fails."""

    def __init__(self, url: str, reason: str):
        super().__init__(f"Failed to download attachment from {url}: {reason}")
        self.url = url
        self.reason = reason


# ──────────────────────────────
# 🧭 Platform and config errors
# ──────────────────────────────


class UnknownPlatformError(CTFBridgeError):
    """Raised when the platform cannot be identified."""

    def __init__(self, url: str):
        super().__init__(f"Could not identify platform at URL: {url}")
        self.url = url


class UnknownBaseURLError(CTFBridgeError):
    """Raised when no base URL is configured or available."""

    def __init__(self, url: str):
        super().__init__(f"Could not determine base URL from {url}")
        self.url = url
