from ctfbridge.utils.platform_detection import detect_platform
from .exceptions import UnknownPlatformError

def get_client(base_url: str):
    """Return the appropriate platform client based on auto-detection."""
    platform = detect_platform(base_url)

    if platform == "demo":
        from ctfbridge.clients.demo_client import DemoClient
        return DemoClient(base_url)

    elif platform == "CTFd":
        from ctfbridge.clients.ctfd_client import CTFdClient
        return CTFdClient(base_url)

    raise UnknownPlatformError(f"No client available for platform {platform}")