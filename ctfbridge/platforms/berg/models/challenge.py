"""Models for CTFd challenge data"""

from typing import List, Optional

from pydantic import BaseModel, Field

from ctfbridge.models.challenge import Attachment, Challenge, DownloadType, DownloadInfo


class BergAttachment(BaseModel):
    """Model for a single attachment from the Berg CTF API"""

    file_name: str = Field(..., alias="fileName")
    download_url: str = Field(..., alias="downloadUrl")


class BergChallenge(BaseModel):
    """Model for Berg CTF challenge data"""

    name: str
    display_name: str = Field(..., alias="displayName")
    author: str
    description: str
    hide_until: str | None = Field(None, alias="hideUntil")
    categories: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    event: str
    difficulty: str
    flag_format: Optional[str] = Field(None, alias="flagFormat")
    attachments: List[BergAttachment] = Field(default_factory=list)
    has_remote: bool = Field(..., alias="hasRemote")

    def to_core_model(self) -> Challenge:
        core_attachments = [
            Attachment(
                name=attachment.file_name,
                download_info=DownloadInfo(
                    type=DownloadType.HTTP,
                    url=attachment.download_url,
                ),
            )
            for attachment in self.attachments
        ]

        return Challenge.model_construct(
            id=self.name,
            name=self.display_name,
            categories=self.categories,
            description=self.description,
            attachments=core_attachments,
            solved=False,
            tags=self.tags,
            difficulty=self.difficulty,
            flag_format=self.flag_format,
        )
