from abc import ABC, abstractmethod
from ctfbridge.base.services.session import SessionHelper
from ctfbridge.base.services.auth import AuthService
from ctfbridge.base.services.attachment import AttachmentService
from ctfbridge.base.services.challenge import ChallengeService
from ctfbridge.base.services.scoreboard import ScoreboardService


class CTFClient(ABC):
    """
    CTF platform client.

    Provides common interface methods and service properties for interacting
    with challenges, authentication, attachments, and scoreboard APIs.
    """

    @property
    @abstractmethod
    def auth(self) -> AuthService | None:
        """Authentication service."""
        pass

    @property
    @abstractmethod
    def attachments(self) -> AttachmentService | None:
        """Attachment handling service."""
        pass

    @property
    @abstractmethod
    def challenges(self) -> ChallengeService | None:
        """Challenge interaction service."""
        pass

    @property
    @abstractmethod
    def scoreboard(self) -> ScoreboardService | None:
        """Scoreboard service."""
        pass

    @property
    @abstractmethod
    def session(self) -> SessionHelper | None:
        """Session helper for managing cookies, headers, etc."""
        pass
