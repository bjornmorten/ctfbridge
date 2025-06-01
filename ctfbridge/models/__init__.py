from .auth import TokenLoginResponse
from .challenge import Attachment, Challenge
from .config import CTFConfig
from .error import ErrorResponse
from .scoreboard import ScoreboardEntry
from .submission import SubmissionResult
from .user import Team, User

__all__ = [
    "Challenge",
    "Attachment",
    "SubmissionResult",
    "ScoreboardEntry",
    "User",
    "Team",
    "TokenLoginResponse",
    "CTFConfig",
    "ErrorResponse",
]
