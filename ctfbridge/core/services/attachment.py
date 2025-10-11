import asyncio
import logging
from pathlib import Path
from stat import S_ISDIR
from typing import Callable
from urllib.parse import urljoin, urlparse

import time
import httpx

from ctfbridge.models.challenge import (
    Attachment,
    AttachmentCollection,
    Challenge,
    DownloadType,
    ProgressData,
)
from ctfbridge.exceptions import AttachmentDownloadError

logger = logging.getLogger(__name__)


class CoreAttachmentService:
    """Handles downloading attachments, returning updated Challenge objects."""

    def __init__(self, client):
        self._client = client
        self._http = httpx.AsyncClient(follow_redirects=True)

    async def download(
        self,
        attachment: Attachment,
        save_dir: str | Path,
        progress: Callable[[ProgressData], None] | None = None,
    ) -> list[Attachment]:
        """
        Download a single attachment (HTTP or SSH).
        Returns one or more Attachment objects.
        """
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        try:
            if attachment.download_info.type == DownloadType.HTTP:
                path = await self._download_http(attachment, save_dir, progress)
                enriched = await self._enrich_metadata(attachment, path)
                return [enriched]

            elif attachment.download_info.type == DownloadType.SSH:
                return await self._download_ssh(attachment, save_dir)

            else:
                raise AttachmentDownloadError(
                    None, f"Unsupported download type: {attachment.download_info.type}"
                )

        except Exception as e:
            logger.warning("Failed to download %s: %s", attachment.name or "<unknown>", e)
            return [attachment]

    async def download_all(
        self,
        challenge: Challenge,
        save_dir: str | Path,
        concurrency: int = 5,
        progress: Callable[[ProgressData], None] | None = None,
    ) -> Challenge:
        """Download all attachments for a given challenge, merging multiple results."""
        attachments = list(challenge.attachments)
        if not attachments:
            logger.debug("Challenge '%s' has no attachments.", challenge.name)
            return challenge

        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        semaphore = asyncio.Semaphore(concurrency)

        async def task(att: Attachment):
            async with semaphore:
                return await self.download(att, save_dir, progress)

        results_nested = await asyncio.gather(*(task(a) for a in attachments))
        results = [att for sublist in results_nested for att in sublist]

        return challenge.model_copy(
            update={"attachments": AttachmentCollection(attachments=results)}
        )

    async def _download_http(
        self,
        attachment: Attachment,
        save_dir: Path,
        progress: Callable[[ProgressData], None] | None = None,
    ) -> Path:
        """Download a single HTTP/HTTPS attachment."""
        url = self._normalize_url(attachment.download_info.url)
        filename = attachment.name or Path(urlparse(url).path).name
        final_path = save_dir / filename
        temp_path = final_path.with_suffix(final_path.suffix + ".part")

        async with self._http.stream("GET", url) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            start_time = time.monotonic()

            with temp_path.open("wb") as f:
                async for chunk in response.aiter_bytes(1048576):
                    f.write(chunk)
                    downloaded += len(chunk)

                    elapsed = time.monotonic() - start_time
                    speed_bps = downloaded / elapsed if elapsed > 0 else 0.0
                    eta_seconds = (total_size - downloaded) / speed_bps if speed_bps > 0 else None

                    if progress and total_size > 0:
                        await progress(
                            ProgressData(
                                attachment=attachment,
                                downloaded_bytes=downloaded,
                                total_bytes=total_size,
                                percentage=(downloaded / total_size) * 100,
                                speed_bps=speed_bps,
                                eta_seconds=eta_seconds,
                            )
                        )

        if final_path.exists():
            logger.warning("File already exists and will be overwritten: %s", final_path)

        temp_path.rename(final_path)
        logger.info("Downloaded HTTP file: %s", final_path)
        return final_path

    async def _download_ssh(self, attachment: Attachment, save_dir: Path) -> list[Attachment]:
        """Download a file or directory from an SSH server, returning one or more Attachment objects."""
        import asyncssh

        info = attachment.download_info
        if not info or not info.host or not info.path or not info.username:
            raise AttachmentDownloadError(None, "Incomplete SSH download info")

        save_dir.mkdir(parents=True, exist_ok=True)
        downloaded: list[Attachment] = []

        async with asyncssh.connect(
            info.host,
            port=info.port or 22,
            username=info.username,
            password=info.password,
            known_hosts=None,
            client_keys=[info.key] if info.key else None,
        ) as conn:
            try:
                sftp = await asyncio.wait_for(conn.start_sftp_client(), timeout=3)
            except asyncio.TimeoutError:
                raise AttachmentDownloadError(info.path or info.host, "SFTP unavailable.")

            try:
                attrs = await sftp.stat(info.path)
            except (OSError, asyncssh.SFTPError) as e:
                raise AttachmentDownloadError(info.path, f"Cannot stat remote path: {e}")

            if S_ISDIR(attrs.permissions):
                logger.info("Remote path '%s' is a directory, downloading contents...", info.path)
                downloaded = await self._download_ssh_dir(sftp, attachment, info.path, save_dir)
            else:
                att = await self._download_ssh_file(sftp, attachment, info.path, save_dir)
                downloaded.append(att)

        return downloaded

    async def _download_ssh_file(
        self, sftp, attachment: Attachment, remote_path: str, local_dir: Path
    ) -> Attachment:
        """Download a single SSH file and return an Attachment with metadata."""
        filename = Path(remote_path).name
        local_path = local_dir / filename
        local_path.parent.mkdir(parents=True, exist_ok=True)

        if local_path.exists():
            logger.warning("File already exists and will be overwritten: %s", local_path)

        await asyncio.wait_for(sftp.get(remote_path, str(local_path)))
        logger.debug("Downloaded SSH file: %s", local_path)

        updated_attachment = attachment.model_copy(
            update={
                "local_path": str(local_path),
                "download_info": attachment.download_info.model_copy(
                    update={"path": remote_path or attachment.download_info.path}
                ),
            }
        )

        updated_attachment = await self._enrich_metadata(updated_attachment, local_path)

        return updated_attachment

    async def _download_ssh_dir(
        self,
        sftp,
        attachment: Attachment,
        remote_dir: str,
        local_dir: Path,
        include_hidden: bool = False,
        seen: set[str] | None = None,
    ) -> list[Attachment]:
        """Recursively download a directory and return a list of Attachment objects."""
        seen = seen or set()
        if remote_dir in seen:
            return []
        seen.add(remote_dir)

        attachments: list[Attachment] = []
        local_dir.mkdir(parents=True, exist_ok=True)

        try:
            entries = await asyncio.wait_for(sftp.listdir(remote_dir), timeout=5)
        except Exception as e:
            logger.warning("Failed to list directory %s: %s", remote_dir, e)
            return []

        for entry in entries:
            if not include_hidden and entry.startswith("."):
                continue

            remote_path = f"{remote_dir.rstrip('/')}/{entry}"
            local_path = local_dir / entry

            try:
                attrs = await asyncio.wait_for(sftp.stat(remote_path), timeout=5)
            except Exception as e:
                logger.warning("Failed to stat %s: %s", remote_path, e)
                continue

            if S_ISDIR(attrs.permissions):
                sub_attachments = await self._download_ssh_dir(
                    sftp, attachment, remote_path, local_path, include_hidden, seen
                )
                attachments.extend(sub_attachments)
            else:
                try:
                    att = await self._download_ssh_file(sftp, attachment, remote_path, local_dir)
                    attachments.append(att)
                except Exception as e:
                    logger.warning("Failed to download %s: %s", remote_path, e)

        return attachments

    async def _enrich_metadata(self, attachment: Attachment, path: Path) -> Attachment:
        """Fill in metadata (name, size) after download."""
        try:
            if path.is_dir():
                return attachment.model_copy(update={"local_path": str(path)})

            size_bytes = path.stat().st_size
            name = attachment.name or path.name

            return attachment.model_copy(
                update={
                    "name": name,
                    "local_path": str(path),
                    "size_bytes": size_bytes,
                }
            )
        except Exception as e:
            logger.warning("Failed to enrich metadata for %s: %s", path, e)
            return attachment

    def _normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        if not parsed.scheme and not parsed.netloc:
            return urljoin(self._client.platform_url.rstrip("/") + "/", url.lstrip("/"))
        return url

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self._http.aclose()
