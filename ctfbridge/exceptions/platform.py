from .base import CTFBridgeError


class UnknownPlatformError(CTFBridgeError):
    def __init__(self, url: str):
        super().__init__(f"Could not identify platform at URL: {url}")
        self.url = url


class UnknownBaseURLError(CTFBridgeError):
    def __init__(self, url: str):
        super().__init__(f"Could not determine base URL from {url}")
        self.url = url


class PlatformMismatchError(CTFBridgeError):
    def __init__(self, platform: str, expected: str):
        super().__init__(f"Expected platform '{expected}', but got '{platform}'")
        self.platform = platform
        self.expected = expected
