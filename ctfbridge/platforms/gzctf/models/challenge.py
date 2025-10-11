from pathlib import Path
from typing import List

from pydantic import BaseModel, Field

from ctfbridge.models.challenge import (
    Attachment,
    Challenge,
    DownloadInfo,
    DownloadType,
    AttachmentCollection,
)
from ctfbridge.models.submission import SubmissionResult


class GZCTFContext(BaseModel):
    url: str | None = Field(...)
    fileSize: int | None = Field(...)


class GZCTFChallenge(BaseModel):
    id: int
    title: str
    category: str
    score: int
    content: str | None = None
    tags: List[str] = Field(default_factory=list)
    context: GZCTFContext | None = Field(None)

    # Custom value parsed from rank.
    is_solved: bool

    def to_core_model(self) -> Challenge:
        return Challenge.model_construct(
            id=self.id,
            name=self.title,
            categories=[self.category],
            description=self.content,
            attachments=AttachmentCollection(
                attachments=[
                    Attachment(
                        name=Path(self.context.url).name,
                        download_info=DownloadInfo(
                            type=DownloadType.HTTP,
                            url=self.context.url,
                        ),
                    )
                    if self.context and self.context.url
                    else []
                ]
            ),
            solved=self.is_solved,
        )


class GZCTFSubmission(BaseModel):
    correct: bool
    message: str

    def to_core_model(self) -> SubmissionResult:
        return SubmissionResult.model_construct(correct=self.correct, message=self.message)
