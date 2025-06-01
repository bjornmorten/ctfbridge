from typing import List, Optional
from pydantic import BaseModel, Field
from ctfbridge.models import Challenge as CoreChallenge, Attachment as CoreAttachment
from ctfbridge.models.submission import SubmissionResult as CoreSubmissionResult


class RCTFFile(BaseModel):
    name: str
    url: str

    def to_core_model(self) -> CoreAttachment:
        return CoreAttachment(name=self.name, url=self.url)


class RCTFChallengeData(BaseModel):
    id: str
    name: str
    category: str
    description: str
    points: int
    author: Optional[str] = None
    files: List[RCTFFile] = Field(default_factory=list)
    # Add any other fields rCTF provides for a challenge
    # e.g., tags, hints, etc.

    def to_core_model(self, solved: bool) -> CoreChallenge:
        return CoreChallenge.model_construct(
            id=self.id,
            name=self.name,
            categories=[self.category] if self.category else [],
            value=self.points,
            description=self.description,
            attachments=[file.to_core_model() for file in self.files],
            authors=[self.author] if self.author else [],
            solved=solved,
            # Map other fields if available
        )


class RCTFSubmissionResponse(BaseModel):
    kind: str  # e.g., "goodFlag", "badFlag", "alreadySolvedChallenge"
    message: str
    # data: Optional[Any] = None # If rCTF includes additional data

    def to_core_model(self) -> CoreSubmissionResult:
        is_correct = self.kind == "goodFlag" or self.message.lower().startswith(
            "correct"
        )  # Adjust based on rCTF's actual responses
        return CoreSubmissionResult(correct=is_correct, message=self.message)
