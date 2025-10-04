import asyncio
import logging
import os
import time
from typing import Callable, List, Optional
from urllib.parse import urljoin, urlparse

import httpx

from ctfbridge.base.services.attachment import AttachmentService
from ctfbridge.exceptions import AttachmentDownloadError
from ctfbridge.models.challenge import Attachment, ProgressData

logger = logging.getLogger(__name__)


class CoreAttachmentService(AttachmentService):
    """
    Core implementation of the attachment service.
    Provides functionality for downloading challenge attachments from both platform and external URLs.
    """

    def __init__(self, client):
        self._client = client
        self._external_http = httpx.AsyncClient(follow_redirects=True)

    async def download(
        self,
        attachment: Attachment,
        save_dir: str,
        filename: Optional[str] = None,
        progress: Optional[Callable[[ProgressData], None]] = None,
    ) -> str:
        os.makedirs(save_dir, exist_ok=True)

        url = self._normalize_url(attachment.url)
        final_filename = filename or attachment.name
        final_path = os.path.join(save_dir, final_filename)
        temp_path = final_path + ".part"

        logger.info("Downloading attachment from %s to %s", url, temp_path)

        try:
            client = self._external_http if self._is_external_url(url) else self._client._http
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                await self._save_stream_to_file(response, temp_path, progress, attachment)

            os.rename(temp_path, final_path)
            logger.info("Successfully downloaded and moved to: %s", final_path)

        except Exception as e:
            logger.error("Download failed for %s: %s", url, e)
            raise AttachmentDownloadError(url, str(e)) from e
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return final_path

    async def download_all(
        self,
        attachments: List[Attachment],
        save_dir: str,
        progress: Optional[Callable[[ProgressData], None]] = None,
        concurrency: int = 5,
    ) -> List[str]:
        semaphore = asyncio.Semaphore(concurrency)

        async def download_with_semaphore(att: Attachment):
            async with semaphore:
                try:
                    return await self.download(att, save_dir, progress=progress)
                except AttachmentDownloadError as e:
                    logger.warning("Skipping attachment '%s': %s", att.name, e)
                    return None

        tasks = [download_with_semaphore(att) for att in attachments]
        results = await asyncio.gather(*tasks)
        return [path for path in results if path]

    async def _save_stream_to_file(
        self,
        response: httpx.Response,
        path: str,
        progress: Optional[Callable[[ProgressData], None]],
        attachment: Attachment,
    ):
        total_size = int(response.headers.get("Content-Length", 0))
        downloaded_size = 0
        start_time = time.time()

        try:
            with open(path, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=10485760):
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    if progress and total_size > 0:
                        elapsed_time = time.time() - start_time

                        if elapsed_time == 0:
                            elapsed_time = 0.001

                        speed = downloaded_size / elapsed_time
                        eta = (total_size - downloaded_size) / speed if speed > 0 else None
                        percent = (downloaded_size / total_size) * 100

                        progress_data = ProgressData(
                            attachment=attachment,
                            downloaded_bytes=downloaded_size,
                            total_bytes=total_size,
                            percentage=percent,
                            speed_bps=speed,
                            eta_seconds=eta,
                        )
                        await progress(progress_data)
        except Exception as e:
            raise OSError(f"Failed to save file to {path}: {e}") from e

    def _normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        if not parsed.scheme and not parsed.netloc:
            return urljoin(self._client.platform_url.rstrip("/") + "/", url.lstrip("/"))
        return url

    def _is_external_url(self, url: str) -> bool:
        base_netloc = urlparse(self._client.platform_url).netloc
        target_netloc = urlparse(url).netloc
        return base_netloc != target_netloc

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self._external_http.aclose()
