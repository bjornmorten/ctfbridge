from .attachment import AttachmentDownloadError
from .auth import (
    InvalidAuthMethodError,
    LoginError,
    MissingAuthMethodError,
    NotAuthenticatedError,
    NotAuthorizedError,
    SessionExpiredError,
    TokenAuthError,
)
from .base import CTFBridgeError
from .challenge import (
    ChallengeFetchError,
    ChallengesUnavailableError,
    CTFInactiveError,
    SubmissionError,
)
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
    "NotAuthenticatedError",
    "NotAuthorizedError",
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
    "ChallengesUnavailableError",
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
