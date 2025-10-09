from typing import List

from pydantic import BaseModel, Field

from ctfbridge.models.challenge import Attachment, Challenge, Service


class CryptoHackCategory(BaseModel):
    name: str = Field(..., description="Display name of the category")
    path: str = Field(..., description="Relative path")


class CryptoHackAttachment(BaseModel):
    name: str = Field(...)
    path: str = Field(...)


class CryptoHackChallenge(BaseModel):
    id: str
    name: str
    description: str
    category: str
    subcategory: str
    authors: List[str]
    attachments: List[CryptoHackAttachment]
    service: Service | None
    flag_format: str | None
    points: int
    solved: bool

    def to_core_model(self) -> Challenge:
        return Challenge.model_construct(
            id=self.id,
            name=self.name,
            solved=self.solved,
            categories=[self.category],
            subcategory=self.subcategory,
            description=self.description,
            value=self.points,
            flag_format=self.flag_format,
            attachments=[
                Attachment(name=attachment.name, url=attachment.path)
                for attachment in self.attachments
            ],
            services=[self.service] if self.service else [],
        )
