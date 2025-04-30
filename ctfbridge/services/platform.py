from abc import abstractmethod


class PlatformService:
    """
    Service to expose platform-level metadata like version, capabilities, name, etc.

    This is designed to be attached to any CTFPlatformClient as `client.platform`.
    """

    def __init__(self, client):
        self.client = client

    @abstractmethod
    def get_name(self) -> str:
        """Return the static platform name declared by the client."""
        pass

    def get_version(self) -> str:
        """Return the platform version string, if available."""
        raise NotImplementedError("Platform version not implemented.")

    def get_ctf_name(self) -> str:
        """Return the name of the CTF event/platform."""
        raise NotImplementedError("CTF name not implemented")

    def get_theme(self) -> str:
        """Return the active platform theme (CTFd-specific)."""
        raise NotImplementedError("CTF theme not implemented")
