from abc import abstractmethod


class PlatformService:
    """
    Service for retrieving platform-level metadata such as name, version,
    capabilities, and theme.
    """

    def __init__(self, client):
        """
        Initialize the platform service.

        Args:
            client: A reference to the CTF platform client.
        """
        self.client = client

    @abstractmethod
    def get_name(self) -> str:
        """
        Return the static platform name declared by the client.

        Returns:
            str: The platform name (e.g., "CTFd", "FBCTF").
        """
        pass

    def get_version(self) -> str:
        """
        Return the platform version string, if available.

        This method is optional and may be overridden by platform-specific implementations.

        Returns:
            str: The platform version string.

        Raises:
            NotImplementedError: If the platform does not provide a version.
        """
        raise NotImplementedError("Platform version not implemented.")

    def get_ctf_name(self) -> str:
        """
        Return the name of the CTF event or platform instance.

        Useful for identifying the branding of a specific deployment.

        Returns:
            str: The CTF event or instance name.

        Raises:
            NotImplementedError: If the name is not provided by the platform.
        """
        raise NotImplementedError("CTF name not implemented")

    def get_theme(self) -> str:
        """
        Return the name of the CTF event or platform instance.

        Useful for identifying the branding of a specific deployment.

        Returns:
            str: The CTF event or instance name.

        Raises:
            NotImplementedError: If the name is not provided by the platform.
        """
        raise NotImplementedError("CTF theme not implemented")
