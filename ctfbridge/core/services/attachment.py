import logging
import os
from typing import List, Optional
from urllib.parse import urljoin, urlparse

import httpx

from ctfbridge.base.services.attachment import AttachmentService
from ctfbridge.exceptions import AttachmentDownloadError
from ctfbridge.models.challenge import Attachment

logger = logging.getLogger(__name__)


class CoreAttachmentService(AttachmentService):
    """
    Core implementation of the attachment service.
    Provides functionality for downloading challenge attachments from both platform and external URLs.
    """

    def __init__(self, client):
        """
        Initialize the attachment service.

        Args:
            client: The CTF client instance
        """
        self._client = client
        self._external_http = httpx.AsyncClient(follow_redirects=True)

    async def download(
        self, attachment: Attachment, save_dir: str, filename: Optional[str] = None
    ) -> str:
        """
        Download a single attachment to the specified directory.

        Args:
            attachment: The attachment to download
            save_dir: Directory to save the file in
            filename: Optional custom filename (defaults to attachment name)

        Returns:
            Path to the downloaded file

        Raises:
            AttachmentDownloadError: If the download fails
        """
        os.makedirs(save_dir, exist_ok=True)

        url = self._normalize_url(attachment.url)
        final_filename = filename or attachment.name
        save_path = os.path.join(save_dir, final_filename)

        logger.info("Downloading attachment from %s to %s", url, save_path)

        try:
            client = self._external_http if self._is_external_url(url) else self._client._http
            async with client.stream("GET", url) as response:
                await self._save_stream_to_file(response, save_path)
            logger.info("Successfully downloaded: %s", save_path)
        except Exception as e:
            logger.error("Download failed for %s: %s", url, e)
            raise AttachmentDownloadError(url, str(e)) from e

        return save_path

    async def download_all(self, attachments: List[Attachment], save_dir: str) -> List[str]:
        """
        Download multiple attachments to the specified directory.

        Args:
            attachments: List of attachments to download
            save_dir: Directory to save the files in

        Returns:
            List of paths to successfully downloaded files
        """
        paths = []
        for att in attachments:
            try:
                path = await self.download(att, save_dir)
                paths.append(path)
            except AttachmentDownloadError as e:
                logger.debug("Skipping attachment '%s': %s", att.name, e)
        return paths

    def _normalize_url(self, url: str) -> str:
        """
        Convert relative URLs to absolute URLs using the platform base URL.

        Args:
            url: The URL to normalize

        Returns:
            Absolute URL
        """
        parsed = urlparse(url)
        if not parsed.scheme and not parsed.netloc:
            # It's a relative path → join with the platform base URL
            return urljoin(self._client.platform_url.rstrip("/") + "/", url.lstrip("/"))
        return url

    def _is_external_url(self, url: str) -> bool:
        """
        Check if a URL points to an external domain.

        Args:
            url: The URL to check

        Returns:
            True if the URL is external, False if it's on the platform domain
        """
        base_netloc = urlparse(self._client.platform_url).netloc
        target_netloc = urlparse(url).netloc
        return base_netloc != target_netloc

    async def _save_stream_to_file(self, response: httpx.Response, path: str):
        """
        Save a streaming response to a file.

        Args:
            response: The HTTP response to stream from
            path: Path to save the file to

        Raises:
            OSError: If writing to the file fails
        """
        try:
            with open(path, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=10485760):
                    f.write(chunk)
        except Exception as e:
            raise OSError(f"Failed to save file to {path}: {e}") from e

    async def __aenter__(self):
        """Enter the async context manager."""
        return self

    async def __aexit__(self, *args):
        """Exit the async context manager and close the external HTTP client."""
        await self._external_http.aclose()
