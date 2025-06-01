from typing import Optional, List
from pydantic import BaseModel
from ctfbridge.models.challenge import Challenge, Attachment


class RCTFChallengeFile(BaseModel):
    url: str
    name: str


class RCTFChallengeData(BaseModel):
    id: str
    name: str
    description: Optional[str]
    category: str
    author: str
    points: int
    solves: int
    files: List[RCTFChallengeFile] = []

    def to_core_model(self, solved: bool = False) -> Challenge:
        return Challenge.model_construct(
            id=self.id,
            name=self.name,
            value=self.points,
            categories=[self.category],
            description=self.description,
            attachments=[Attachment(name=f.name, url=f.url) for f in self.files],
            solved=solved,
            tags=[],
        )
