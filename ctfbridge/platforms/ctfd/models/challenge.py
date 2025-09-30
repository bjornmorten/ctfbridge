"""Models for CTFd challenge data"""

from typing import Any
from urllib.parse import unquote, urlparse
from pydantic import BaseModel, Field

from ctfbridge.models.challenge import Challenge, Attachment
from ctfbridge.models.submission import SubmissionResult
from ctfbridge.processors.helpers.services import extract_services_from_text


class CTFdChallenge(BaseModel):
    """Model for CTFd challenge data"""

    id: int
    type: str
    name: str
    value: int
    category: str
    description: str | None = None
    connection_info: str | None = None
    solved_by_me: bool = False
    max_attempts: int = 0
    attempts: int = 0
    tags: list[dict[str, str] | str] = Field(default_factory=list)
    files: list[str] = Field(default_factory=list)
    hints: list[dict[str, Any]] = Field(default_factory=list)

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
            services=(
                extract_services_from_text(self.connection_info) if self.connection_info else []
            ),
            solved=self.solved_by_me,
            tags=[tag["value"] if isinstance(tag, dict) else tag for tag in self.tags],
        )


class CTFdSubmission(BaseModel):
    """Model for CTFd submission response data"""

    status: str | None = None
    message: str = "No message provided"

    def to_core_model(self) -> SubmissionResult:
        """Convert to core SubmissionResult model"""
        print(self.status, self.message)
        # If status is None, this is likely an error response
        is_correct = (self.status is not None and self.status.lower() == "correct") or (
            self.message.lower().startswith("correct")
        )
        return SubmissionResult.model_construct(correct=is_correct, message=self.message)
