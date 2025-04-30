class CTFBridgeError(Exception):
    """Base class for all CTFBridge exceptions."""

class LoginError(CTFBridgeError):
    """Raised when login fails."""

class ChallengeFetchError(CTFBridgeError):
    """Raised when fetching challenges fails."""

class SubmissionError(CTFBridgeError):
    """Raised when submitting a flag fails."""

class SessionExpiredError(CTFBridgeError):
    """Raised when session has expired or authentication failed."""

class RateLimitError(CTFBridgeError):
    """Raised when the server enforces rate limiting (HTTP 429)."""

class UnknownPlatformError(CTFBridgeError):
    """Raised when the platform cannot be identified."""

class UnknownBaseURL(CTFBridgeError):
    """Raised when the platform cannot be identified."""
