from pydantic import BaseModel, Field

from ctfbridge.models.challenge import Attachment, Challenge
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.platforms.htb.http.endpoints import Endpoints


class HTBContext(BaseModel):
    url: str | None = Field(...)
    fileSize: int | None = Field(...)


class HTBChallenge(BaseModel):
    id: int
    name: str
    points: int
    challenge_category_id: int
    description: str
    content: str | None = None
    creator: str
    filename: str
    solved: bool

    # FETCH FROM OTHER ENDPOINT
    category: None = None

    def to_core_model(self) -> Challenge:
        return Challenge.model_construct(
            id=str(self.id),
            name=self.name,
            categories=[self.category],
            description=self.content,
            attachments=[
                Attachment(
                    name=self.filename,
                    url=Endpoints.Challenges.download_attachment_url(self.id),
                )
            ]
            if self.filename
            else [],
            authors=[self.creator],
            solved=self.solved,
        )


class HTBSubmission(BaseModel):
    correct: bool
    message: str

    def to_core_model(self) -> SubmissionResult:
        return SubmissionResult.model_construct(correct=self.correct, message=self.message)
