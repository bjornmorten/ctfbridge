from .base import CTFBridgeError


class AttachmentDownloadError(CTFBridgeError):
    def __init__(self, url: str, reason: str):
        super().__init__(f"Failed to download attachment from {url}: {reason}")
        self.url = url
        self.reason = reason
