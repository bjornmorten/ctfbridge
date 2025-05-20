from typing import List

from pydantic import BaseModel, Field
from enum import Enum


class ServiceType(str, Enum):
    TCP = "tcp"
    UDP = "udp"
    HTTP = "http"
    SSH = "ssh"
    FTP = "ftp"
    TELNET = "telnet"


class Attachment(BaseModel):
    name: str
    url: str


class Service(BaseModel):
    type: ServiceType
    host: str | None = None
    port: int | None = None
    url: str | None = None
    raw: str | None = None


class Tag(BaseModel):
    value: str


class Challenge(BaseModel):
    id: str
    name: str
    categories: List[str] = Field(default_factory=list)
    normalized_categories: List[str] = Field(default_factory=list)
    value: int | None = None
    description: str | None = None
    attachments: List[Attachment] = Field(default_factory=list)
    service: Service | None = None
    tags: List[Tag] = Field(default_factory=list)
    solved: bool | None = False
    author: str | None = None
    difficulty: str | None = None

    @property
    def category(self) -> str | None:
        return self.categories[0] if self.categories else None

    @property
    def normalized_category(self) -> str | None:
        return self.normalized_categories[0] if self.normalized_categories else None

    @property
    def has_attachments(self) -> bool:
        return bool(self.attachments)

    @property
    def has_service(self) -> bool:
        return self.service is not None
