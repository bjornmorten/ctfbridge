import os
from typing import List, Optional

import requests

from ctfbridge.models.challenge import Attachment
from ctfbridge.utils.network import is_external_url


class AttachmentService:
    """
    Service for handling file downloads for attachments.
    Handles session-aware and unauthenticated downloads.
    """

    def __init__(self, client):
        self.client = client

    def download(self, attachment: Attachment, save_dir: str, filename: Optional[str] = None) -> str:
        """Download an attachment and save it locally."""
        os.makedirs(save_dir, exist_ok=True)

        url = attachment.url
        final_filename = filename or attachment.name
        save_path = os.path.join(save_dir, final_filename)

        # Use session if URL is from same domain
        if not is_external_url(self.client.base_url, url):
            resp = self.client.session.get(url, stream=True)
        else:
            resp = requests.get(url, stream=True)

        if resp.status_code != 200:
            raise Exception(f"Failed to download attachment: {url} (status {resp.status_code})")

        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=10485760):
                if chunk:
                    f.write(chunk)

        return save_path

    def download_all(self, attachments: List[Attachment], save_dir: str) -> List[str]:
        """Download all attachments to a directory."""
        return [self.download(att, save_dir) for att in attachments]
