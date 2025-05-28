from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlparse, urlunparse

import httpx


class PlatformIdentifier(ABC):
    """
    Abstract base class for CTF platform detection logic.
    Subclasses must implement platform-specific logic for detecting
    whether a given URL belongs to this platform.
    """

    def __init__(self, http: httpx.AsyncClient):
        self.http = http

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """
        Name of the platform (e.g., 'CTFd', 'rCTF').
        """
        pass

    @abstractmethod
    def match_url_pattern(self, url: str) -> bool:
        """
        Fast string-based check to determine if this platform should be considered.
        Should not make network calls.

        Return:
            True if this identifier might match the URL, else False.
        """
        pass

    @abstractmethod
    async def static_detect(self, response: httpx.Response) -> Optional[bool]:
        """
        Inspect the HTTP response (HTML, headers, etc.) to quickly confirm or rule out the platform.

        Return:
            - True: Definitely this platform
            - False: Definitely not this platform
            - None: Inconclusive
        """
        pass

    @abstractmethod
    async def is_base_url(self, candidate: str) -> bool:
        """
        Check if the given candidate URL is the correct base for this platform.

        Typically this checks that a key endpoint exists (e.g., /api/config).

        Return:
            True if it's the base URL, else False.
        """
        pass

    @abstractmethod
    async def dynamic_detect(self, base_url: str) -> bool:
        """
        Full detection using platform-specific requests (e.g., API checks, data validation).

        Should only be called after is_base_url returns True.

        Return:
            True if platform is confirmed, else False.
        """
        pass
