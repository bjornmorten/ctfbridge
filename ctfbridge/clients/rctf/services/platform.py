from ctfbridge.services import PlatformService


class RCTFPlatformService(PlatformService):
    """
    Platform service
    """
    def __init__(self, client):
        super().__init__(client)

    def get_name(self) -> str:
        return "rCTF"