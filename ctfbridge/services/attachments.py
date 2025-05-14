import os
from typing import List, Optional

import requests

from ctfbridge.models.challenge import Attachment
from ctfbridge.utils.network import is_external_url


class AttachmentService:
    """
    Service for handling file downloads for attachments.

    This service provides functionality to download individual or multiple
    attachments, using the client's session for authenticated requests when necessary.
    """

    def __init__(self, client):
        """
        Initialize the attachment service.

        Args:
            client: A reference to the CTF platform client containing session and base URL info.
        """
        self.client = client

    def download(
        self, attachment: Attachment, save_dir: str, filename: Optional[str] = None
    ) -> str:
        """
        Download a single attachment and save it locally.

        If the attachment's URL matches the client's domain, an authenticated session
        is used; otherwise, a direct unauthenticated request is made.

        Args:
            attachment: The attachment to download.
            save_dir: Directory to save the downloaded file.
            filename: Optional override for the filename. If not provided, `attachment.name` is used.

        Returns:
            Full path to the saved file.

        Raises:
            Exception: If the download fails (non-200 response).
        """
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
            raise Exception(
                f"Failed to download attachment: {url} (status {resp.status_code})"
            )

        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=10485760):
                if chunk:
                    f.write(chunk)

        return save_path

    def download_all(self, attachments: List[Attachment], save_dir: str) -> List[str]:
        """
        Download a list of attachments to the specified directory.

        Args:
            attachments: List of attachments to download.
            save_dir: Directory to save the downloaded files.

        Returns:
            List of full paths to the downloaded files.
        """
        return [self.download(att, save_dir) for att in attachments]
