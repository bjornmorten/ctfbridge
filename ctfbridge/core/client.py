from ctfbridge.base.client import CTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.core.services.session import CoreSessionHelper


class CoreCTFClient(CTFClient):
    def __init__(
        self,
        auth: CoreAuthService | None = None,
        attachments: CoreAttachmentService | None = None,
        challenges: CoreChallengeService | None = None,
        scoreboard: CoreScoreboardService | None = None,
        session: CoreSessionHelper | None = None,
    ):
        self._auth = auth
        self._attachments = attachments
        self._challenges = challenges
        self._scoreboard = scoreboard
        self._session = session

    @property
    def auth(self) -> CoreAuthService | None:
        return self._auth

    @property
    def attachments(self) -> CoreAttachmentService | None:
        return self._attachments

    @property
    def challenges(self) -> CoreChallengeService | None:
        return self._challenges

    @property
    def scoreboard(self) -> CoreScoreboardService | None:
        return self._scoreboard

    @property
    def session(self) -> CoreSessionHelper | None:
        return self._session
