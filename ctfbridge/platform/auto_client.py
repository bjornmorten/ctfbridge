from ..clients import CTFdClient, DemoClient, RCTFClient
from ..exceptions import UnknownPlatformError
from .detector import detect_platform


def get_client(input_url: str):
    """
    Automatically detect platform and return the appropriate client.
    """
    platform, base_url = detect_platform(input_url)

    if platform == "CTFd":
        return CTFdClient(base_url)
    elif platform == "rCTF":
        return RCTFClient(base_url)
    elif platform == "demo":
        return DemoClient(base_url)

    raise UnknownPlatformError(f"No client available for platform {platform}")

