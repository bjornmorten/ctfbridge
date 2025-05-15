import os
import logging
from typing import List, Optional
from urllib.parse import urlparse

import httpx
from ctfbridge.models.challenge import Attachment
from ctfbridge.base.services.attachment import AttachmentService
from ctfbridge.exceptions import AttachmentDownloadError

logger = logging.getLogger(__name__)


class CoreAttachmentService(AttachmentService):
    def __init__(self, client):
        self._client = client
        self._external_http = httpx.AsyncClient(follow_redirects=True)

    async def download(
        self, attachment: Attachment, save_dir: str, filename: Optional[str] = None
    ) -> str:
        os.makedirs(save_dir, exist_ok=True)

        url = attachment.url
        final_filename = filename or attachment.name
        save_path = os.path.join(save_dir, final_filename)

        logger.info("Downloading attachment from %s to %s", url, save_path)

        try:
            client = (
                self._external_http
                if self._is_external_url(url)
                else self._client._http
            )
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                await self._save_stream_to_file(response, save_path)
            logger.info("Successfully downloaded: %s", save_path)
        except Exception as e:
            logger.error("Download failed for %s: %s", url, e)
            raise AttachmentDownloadError(url, str(e)) from e

        return save_path

    async def download_all(
        self, attachments: List[Attachment], save_dir: str
    ) -> List[str]:
        paths = []
        for att in attachments:
            try:
                path = await self.download(att, save_dir)
                paths.append(path)
            except AttachmentDownloadError as e:
                logger.warning("Skipping attachment '%s': %s", att.name, e)
        return paths

    def _is_external_url(self, url: str) -> bool:
        base_netloc = urlparse(self._client.platform_url).netloc
        target_netloc = urlparse(url).netloc
        return base_netloc != target_netloc

    async def _save_stream_to_file(self, response: httpx.Response, path: str):
        try:
            with open(path, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=10485760):
                    f.write(chunk)
        except Exception as e:
            raise OSError(f"Failed to save file to {path}: {e}") from e

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self._external_http.aclose()
