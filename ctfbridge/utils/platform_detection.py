from ..exceptions import UnknownPlatformError
import requests

def detect_platform(base_url: str) -> str:
    """Try to detect the CTF platform based on URL."""

    try:
        if base_url == "demo":
            return "demo"

        resp = requests.get(base_url, timeout=5)
        if "Powered by CTFd" in resp.text:
            return "CTFd"

    except Exception:
        pass

    raise UnknownPlatformError(f"Could not detect platform at {base_url}")
