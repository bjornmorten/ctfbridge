from ctfbridge.base import CTFPlatformClient

from .services.attachments import DemoAttachmentService
from .services.auth import DemoAuthService
from .services.challenges import DemoChallengeService
from .services.platform import DemoPlatformService
from .services.scoreboard import DemoScoreboardService

from ctfbridge.models.challenge import Challenge


class DemoClient(CTFPlatformClient):
    logged_in = False


    def __init__(self, base_url: str):
        super().__init__(base_url)

        self.attachments = DemoAttachmentService(self)
        self.auth = DemoAuthService(self)
        self.platform = DemoPlatformService(self)
        self.challenges = DemoChallengeService(self)
        self.scoreboard = DemoScoreboardService(self)