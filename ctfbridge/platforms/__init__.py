from ctfbridge.exceptions import UnknownPlatformError
from ctfbridge.platforms.ctfd.identifier import CTFdIdentifier
from ctfbridge.platforms.rctf.identifier import RCTFIdentifier
from ctfbridge.platforms.registry import get_platform_client

__all__ = ["get_platform_client"]
