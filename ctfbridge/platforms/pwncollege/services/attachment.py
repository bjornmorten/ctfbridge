import logging
import asyncssh
import asyncio
from typing import Callable
from ctfbridge.core.services.attachment import CoreAttachmentService
from ctfbridge.models import Attachment
from pathlib import Path
from ctfbridge.models.challenge import DownloadInfo, DownloadType, ProgressData
from ctfbridge.exceptions import AttachmentDownloadError
from ctfbridge.platforms.pwncollege.utils.api import PwnCollegeService


logger = logging.getLogger(__name__)


class PwnCollegeAttachmentService(CoreAttachmentService):
    """Extends CoreAttachmentService to start on-demand SSH service before download."""

    def __init__(self, client):
        super().__init__(client)
        self.svc = PwnCollegeService(client)
        self._ssh_keypair = None
        self._lock = asyncio.Lock()

    async def download(
        self,
        attachment: Attachment,
        save_dir: str | Path,
        progress: Callable[[ProgressData], None] | None = None,
    ) -> list[Attachment]:
        if attachment.download_info.type == DownloadType.SSH:
            logger.info("Starting SSH service for attachment: %s", attachment.name)

            # We can only run one ondemand instance at a time
            async with self._lock:
                # TODO: fix key leaks. Should remove after we are done.
                private_key, public_key = await self._get_or_create_ssh_keypair()

                attachment.download_info.key = private_key

                try:
                    await self.svc.start_ondemand_docker(
                        attachment.download_info.extra["pwncollege_dojo"],
                        attachment.download_info.extra["pwncollege_module"],
                        attachment.download_info.extra["pwncollege_challenge"],
                    )

                except Exception as e:
                    logger.error("Failed to start SSH service: %s", e)
                    raise AttachmentDownloadError(
                        attachment.name, f"Failed to start SSH server: {e}"
                    )

                attachments = await super().download(attachment, save_dir, progress)

        for att in attachments:
            att.download_info.key = None

        return attachments

    async def _get_or_create_ssh_keypair(self) -> tuple[str, str]:
        """Generate (and cache) an ephemeral SSH keypair."""
        if self._ssh_keypair is None:
            logger.debug("Generating ephemeral SSH keypair")
            key = asyncssh.generate_private_key("ssh-rsa", comment="ctfbridge")
            private_key = key.export_private_key()
            public_key = key.export_public_key()
            self._ssh_keypair = (private_key, public_key)

            await self.svc.add_ssh_key(public_key)
        else:
            logger.debug("Using cached in-memory SSH keypair")
        return self._ssh_keypair
