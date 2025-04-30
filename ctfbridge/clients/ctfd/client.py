from ctfbridge.base import CTFPlatformClient

from .services.attachments import CTFdAttachmentService
from .services.auth import CTFdAuthService
from .services.challenges import CTFdChallengeService
from .services.platform import CTFdPlatformService
from .services.scoreboard import CTFdScoreboardService


class CTFdClient(CTFPlatformClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)

        self.attachments = CTFdAttachmentService(self)
        self.auth = CTFdAuthService(self)
        self.platform = CTFdPlatformService(self)
        self.challenges = CTFdChallengeService(self)
        self.scoreboard = CTFdScoreboardService(self)

