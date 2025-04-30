from ctfbridge.base import CTFPlatformClient

from .services.attachments import RCTFAttachmentService
from .services.auth import RCTFAuthService
from .services.challenges import RCTFChallengeService
from .services.platform import RCTFPlatformService
from .services.scoreboard import RCTFScoreboardService


class RCTFClient(CTFPlatformClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)

        self.attachments = RCTFAttachmentService(self)
        self.auth = RCTFAuthService(self)
        self.platform = RCTFPlatformService(self)
        self.challenges = RCTFChallengeService(self)
        self.scoreboard = RCTFScoreboardService(self)

