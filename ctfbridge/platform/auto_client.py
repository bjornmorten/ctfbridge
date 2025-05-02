from ..base import CTFPlatformClient
from ..clients import CTFdClient, DemoClient, RCTFClient
from ..exceptions import UnknownPlatformError
from .detector import detect_platform


def get_client(input_url: str) -> CTFPlatformClient:
    """
    Automatically detect platform and return the appropriate client.

    This function analyzes the given URL and returns a platform-specific client
    (e.g., CTFdClient, rCTFClient, or DemoClient) that implements the unified
    CTFBridge interface.

    Args:
        input_url (str): The base URL of the CTF platform.

    Returns:
        CTFPlatformClient: A client instance for interacting with the detected platform.

    Raises:
        UnknownPlatformError: If the platform is not supported or cannot be detected.
    """
    platform, base_url = detect_platform(input_url)

    if platform == "CTFd":
        return CTFdClient(base_url)
    elif platform == "rCTF":
        return RCTFClient(base_url)
    elif platform == "demo":
        return DemoClient(base_url)

    raise UnknownPlatformError(f"No client available for platform {platform}")

