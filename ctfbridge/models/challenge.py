from typing import List, Optional

from pydantic import BaseModel, Field


class Attachment(BaseModel):
    name: str
    url: str


class Hint(BaseModel):
    id: int
    content: Optional[str] = None
    cost: int
    unlocked: bool


class Tag(BaseModel):
    value: str


class Challenge(BaseModel):
    id: int | str
    name: str
    category: str
    value: int
    description: str
    attachments: List[Attachment] = Field(default_factory=list)
    hints: List[Hint] = Field(default_factory=list)
    tags: List[Tag] = Field(default_factory=list)
    solved: Optional[bool] = False
    author: Optional[str] = None
