from abc import abstractmethod
from typing import Optional

import httpx

from ctfbridge.base.client import CTFClient
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.core.services.challenge import CoreChallengeService
from ctfbridge.core.services.scoreboard import CoreScoreboardService
from ctfbridge.core.services.session import CoreSessionHelper


class CoreCTFClient(CTFClient):
    """
    Core implementation of the CTF platform client.
    Provides concrete implementations of service properties and HTTP request methods.
    """

    def __init__(
        self,
        auth: CoreAuthService | None = None,
        attachments: CoreAttachmentService | None = None,
        challenges: CoreChallengeService | None = None,
        scoreboard: CoreScoreboardService | None = None,
        session: CoreSessionHelper | None = None,
    ):
        """
        Initialize the core CTF client with optional service instances.

        Args:
            auth: Authentication service instance
            attachments: Attachment handling service instance
            challenges: Challenge interaction service instance
            scoreboard: Scoreboard service instance
            session: Session helper instance
        """
        self._auth = auth
        self._attachments = attachments
        self._challenges = challenges
        self._scoreboard = scoreboard
        self._session = session
        self._http: httpx.AsyncClient

    @property
    def auth(self) -> CoreAuthService | None:
        """Get the authentication service instance."""
        return self._auth

    @property
    def attachments(self) -> CoreAttachmentService | None:
        """Get the attachment handling service instance."""
        return self._attachments

    @property
    def challenges(self) -> CoreChallengeService | None:
        """Get the challenge interaction service instance."""
        return self._challenges

    @property
    def scoreboard(self) -> CoreScoreboardService | None:
        """Get the scoreboard service instance."""
        return self._scoreboard

    @property
    def session(self) -> CoreSessionHelper | None:
        """Get the session helper instance."""
        return self._session

    @property
    @abstractmethod
    def platform_url(self) -> str:
        """
        Get the base URL for the CTF platform.
        Must be implemented by platform-specific clients.
        """
        pass

    def url(self, path: str) -> str:
        """
        Construct a full URL by combining the platform base URL with the given path.

        Args:
            path: The path to append to the platform URL

        Returns:
            The complete URL
        """
        return f"{self.platform_url}{path}"

    async def get(self, path: str, *, params=None, **kwargs):
        """
        Perform a GET request to the platform.

        Args:
            path: The endpoint path
            params: Optional query parameters
            **kwargs: Additional arguments passed to the HTTP client

        Returns:
            The HTTP response
        """
        return await self._http.get(
            self.url(path),
            params=params,
            **kwargs,
        )

    async def post(self, path: str, *, json=None, data=None, headers=None, **kwargs):
        """
        Perform a POST request to the platform.

        Args:
            path: The endpoint path
            json: Optional JSON body
            data: Optional form data
            headers: Optional request headers
            **kwargs: Additional arguments passed to the HTTP client

        Returns:
            The HTTP response
        """
        return await self._http.post(
            self.url(path),
            json=json,
            data=data,
            headers=headers,
            **kwargs,
        )
