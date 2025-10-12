import logging
from typing import Callable
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.models import Attachment
from pathlib import Path
from ctfbridge.models.challenge import DownloadInfo, DownloadType, ProgressData
from ctfbridge.exceptions import AttachmentDownloadError

logger = logging.getLogger(__name__)


class PwnCollegeAttachmentService(CoreAttachmentService):
    """Extends CoreAttachmentService to start on-demand SSH service before download."""

    def __init__(self, client, start_ssh_server: Callable[[Attachment], None]):
        super().__init__(client)
        self._start_ssh_server = start_ssh_server

    async def download(
        self,
        attachment: Attachment,
        save_dir: str | Path,
        progress: Callable[[ProgressData], None] | None = None,
    ) -> list[Attachment]:
        if attachment.download_info.type == DownloadType.SSH:
            logger.info("Starting SSH service for attachment: %s", attachment.name)

            # TODO: CREATE AND SET SSH KEY. Inject into attachment object before super call

            # attachment.download_info.key = public_key

            try:
                # TODO: start SSH service for challenge
                pass
            except Exception as e:
                logger.error("Failed to start SSH service: %s", e)
                raise AttachmentDownloadError(attachment.name, f"Failed to start SSH server: {e}")

        return await super().download(attachment, save_dir, progress)
