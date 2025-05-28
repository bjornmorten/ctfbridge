class CTFBridgeError(Exception):
    """Base class for all CTFBridge errors."""

    def __init__(self, message: str = None):
        super().__init__(message or self.__class__.__name__)

    def __str__(self):
        return self.args[0] if self.args else self.__class__.__name__
