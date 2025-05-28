from .attachment import AttachmentDownloadError
from .auth import (
    InvalidAuthMethodError,
    LoginError,
    MissingAuthMethodError,
    SessionExpiredError,
    TokenAuthError,
)
from .base import CTFBridgeError
from .challenge import ChallengeFetchError, CTFInactiveError, SubmissionError
from .http import (
    APIError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ServiceUnavailableError,
    UnauthorizedError,
    ValidationError,
)
from .platform import PlatformMismatchError, UnknownBaseURLError, UnknownPlatformError
from .scoreboard import ScoreboardFetchError
from .session import SessionError

__all__ = [
    "CTFBridgeError",
    # Auth
    "LoginError",
    "TokenAuthError",
    "MissingAuthMethodError",
    "InvalidAuthMethodError",
    "SessionExpiredError",
    # HTTP
    "APIError",
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "ConflictError",
    "ValidationError",
    "ServerError",
    "ServiceUnavailableError",
    "RateLimitError",
    # Challenge
    "ChallengeFetchError",
    "SubmissionError",
    "CTFInactiveError",
    # Scoreboard
    "ScoreboardFetchError",
    # Session
    "SessionError",
    # Attachments
    "AttachmentDownloadError",
    # Platform
    "UnknownPlatformError",
    "UnknownBaseURLError",
    "PlatformMismatchError",
]
