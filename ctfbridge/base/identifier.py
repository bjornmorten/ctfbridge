from abc import ABC, abstractmethod
import httpx


class PlatformIdentifier(ABC):
    """Abstract base class for platform detection."""

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @abstractmethod
    async def static_detect(self, response: httpx.Response) -> bool:
        """Perform quick static checks to determine if the platform is reachable.

        This method should be used to check for simple platform detection,
        such as HTTP response status or headers.

        Returns:
            bool: True if the platform can be detected using quick checks, False otherwise.

        Raises:
            NotImplementedError: If not implemented in the subclass.
        """
        pass

    @abstractmethod
    async def dynamic_detect(self, base_url: str) -> bool:
        """Perform a full dynamic probe to confirm the platform.

        This method should be used for more detailed checks, such as querying
        specific API endpoints or platform-specific data to fully confirm the platform type.

        Returns:
            bool: True if the platform is confirmed, False otherwise.

        Raises:
            NotImplementedError: If not implemented in the subclass.
        """
        pass

    @abstractmethod
    async def is_base_url(self, candidate: str) -> bool:
        """Confirm if a candidate URL is the actual base of the platform.

        Args:
            candidate: The candidate base URL.

        Returns:
            True if the config endpoint is reachable and valid.
        """
