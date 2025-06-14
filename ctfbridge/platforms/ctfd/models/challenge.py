"""Models for CTFd challenge data"""

from typing import Optional, List, Dict, Any, Union
from urllib.parse import unquote, urlparse
from pydantic import BaseModel, Field

from ctfbridge.models.challenge import Challenge, Attachment
from ctfbridge.models.submission import SubmissionResult


class CTFdChallenge(BaseModel):
    """Model for CTFd challenge data"""

    id: int
    type: str
    name: str
    value: int
    category: str
    description: Optional[str] = None
    connection_info: Optional[str] = None
    solved_by_me: bool = False
    max_attempts: int = 0
    attempts: int = 0
    tags: List[Dict[str, str] | str] = Field(default_factory=list)
    files: List[str] = Field(default_factory=list)
    hints: List[Dict[str, Any]] = Field(default_factory=list)

    def to_core_model(self) -> Challenge:
        """Convert to core Challenge model"""
        return Challenge.model_construct(
            id=str(self.id),
            name=self.name,
            categories=[self.category] if self.category else [],
            value=self.value,
            description=self.description,
            attachments=[
                Attachment(
                    name=unquote(urlparse(url).path.split("/")[-1]),
                    url=url,
                )
                for url in self.files
            ],
            solved=self.solved_by_me,
            tags=[tag["value"] if isinstance(tag, dict) else tag for tag in self.tags],
        )


class CTFdSubmission(BaseModel):
    """Model for CTFd submission response data"""

    status: Optional[str] = None
    message: str = "No message provided"

    def to_core_model(self) -> SubmissionResult:
        """Convert to core SubmissionResult model"""
        # If status is None, this is likely an error response
        is_correct = self.status is not None and self.status.lower() == "correct"
        return SubmissionResult.model_construct(correct=is_correct, message=self.message)
