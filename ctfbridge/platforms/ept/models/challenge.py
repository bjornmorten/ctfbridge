"""Models for EPT challenge data"""

from typing import List
from pydantic import BaseModel, Field

from ctfbridge.models.challenge import Challenge, Attachment
from ctfbridge.platforms.ept.http.endpoints import Endpoints
from ctfbridge.models.submission import SubmissionResult


class EPTAttachment(BaseModel):
    """Model for a single attachment from the EPT CTF API"""

    name: str = Field(...)
    sha256: str = Field(...)


class EPTChallenge(BaseModel):
    """Model for EPT CTF challenge data"""

    id: str
    name: str
    author: str
    description: str
    categories: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    file: EPTAttachment | None = Field(None)
    solved: bool

    def to_core_model(self) -> Challenge:
        return Challenge.model_construct(
            id=self.id,
            name=self.name,
            categories=self.tags,
            description=self.description,
            attachments=[
                Attachment(
                    name=self.file.name,
                    url=Endpoints.Challenges.attachment_download(id=self.id),
                )
            ]
            if self.file
            else [],
            solved=self.solved,
        )


class EPTSubmission(BaseModel):
    """Model for EPT submission response data"""

    correct: bool

    def to_core_model(self) -> SubmissionResult:
        return SubmissionResult.model_construct(correct=self.correct, message=str(self))
