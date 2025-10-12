import logging
from urllib.parse import unquote, urlparse

from ctfbridge.models.challenge import (
    Attachment,
    Challenge,
    AttachmentCollection,
    DownloadInfo,
    DownloadType,
)
from ctfbridge.processors.base import BaseChallengeParser
from ctfbridge.processors.helpers.url_classifier import classify_links
from ctfbridge.processors.helpers.url_extraction import extract_links
from ctfbridge.processors.registry import register_parser

logger = logging.getLogger(__name__)


@register_parser
class AttachmentExtractor(BaseChallengeParser):
    """Extracts attachment URLs from challenge descriptions."""

    def can_handle(self, challenge: Challenge) -> bool:
        """Check if this parser should process the challenge.

        Returns False if the challenge already has attachments or no description.
        """
        return not challenge.has_attachments and bool(challenge.description)

    def _process(self, challenge: Challenge) -> Challenge:
        """Extract attachment URLs from the challenge description.

        Args:
            challenge: The challenge to process.

        Returns:
            The challenge with extracted attachments.
        """
        if not self.can_handle(challenge):
            return challenge

        try:
            desc = challenge.description
            urls = extract_links(desc)
            urls = classify_links(urls)["attachments"]

            # Track seen URLs to avoid duplicates
            seen_urls = set()
            attachments = []

            for url in urls:
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                # Get filename from URL
                parsed = urlparse(url)
                name = unquote(parsed.path.split("/")[-1].split("?")[0])

                attachments.append(
                    Attachment(
                        name=name, download_info=DownloadInfo(type=DownloadType.HTTP, url=url)
                    )
                )

            if attachments:
                challenge.attachments = AttachmentCollection(attachments=attachments)

        except Exception as e:
            logger.error(f"Failed to extract attachments: {e}")

        return challenge
