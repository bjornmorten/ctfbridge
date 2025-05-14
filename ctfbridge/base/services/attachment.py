from typing import List, Optional
from abc import ABC, abstractmethod


from ctfbridge.models.challenge import Attachment


class AttachmentService(ABC):
    """
    Service for handling file downloads for attachments.
    """

    async def download(
        self, attachment: Attachment, save_dir: str, filename: Optional[str] = None
    ) -> str:
        """
        Download a single attachment and save it locally.

        If the attachment's URL matches the client's domain, an authenticated session
        is used; otherwise, a direct unauthenticated request is made.

        Args:
            attachment (Attachment): The attachment to download.
            save_dir (str): Directory to save the downloaded file.
            filename (Optional[str]): Optional override for the filename. If not provided, `attachment.name` is used.

        Returns:
            str: Full path to the saved file.

        Raises:
            Exception: If the download fails (non-200 response).
        """
        raise NotImplementedError

    async def download_all(
        self, attachments: List[Attachment], save_dir: str
    ) -> List[str]:
        """
        Download a list of attachments to the specified directory.

        Args:
            attachments (List[Attachment]): List of attachments to download.
            save_dir (str): Directory to save the downloaded files.

        Returns:
            List[str]: List of full paths to the downloaded files.
        """
        raise NotImplementedError
