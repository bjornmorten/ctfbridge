import os
import shutil
from pathlib import Path
from typing import Optional

from ctfbridge.models import Attachment
from ctfbridge.services import AttachmentService


class DemoAttachmentService(AttachmentService):
    """
    Service for handling file downloads for attachments.
    """

    def __init__(self, client):
        super().__init__(client)

    def download(self, attachment: Attachment, save_dir: str, filename: Optional[str] = None) -> str:
        os.makedirs(save_dir, exist_ok=True)

        platform = self.client.demo_platform
        file_path = platform.attachments_map.get(attachment.url)

        if not file_path or not file_path.exists():
            raise FileNotFoundError(f"Attachment not found: {attachment.url}")

        final_filename = filename or attachment.name
        destination = Path(save_dir) / final_filename

        shutil.copy(file_path, destination)

        return str(destination)
