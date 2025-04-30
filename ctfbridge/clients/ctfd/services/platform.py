from ctfbridge.services import PlatformService


class CTFdPlatformService(PlatformService):
    """
    Platform service
    """
    def __init__(self, client):
        super().__init__(client)

    def get_name(self) -> str:
        return "CTFd"