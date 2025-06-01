from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class ServiceType(str, Enum):
    """Enumeration of possible service types for CTF challenges."""

    TCP = "tcp"
    UDP = "udp"
    HTTP = "http"
    SSH = "ssh"
    FTP = "ftp"
    TELNET = "telnet"


class Attachment(BaseModel):
    """Represents a downloadable attachment file for a challenge."""

    name: str = Field(..., description="The display name of the attachment file.")
    url: str = Field(..., description="The URL from which the attachment can be downloaded.")


class Service(BaseModel):
    """Describes a network service associated with a challenge (e.g., nc host port, http URL)."""

    type: ServiceType = Field(..., description="The type of the network service (e.g., tcp, http).")
    host: str | None = Field(
        None, description="The hostname or IP address of the service, if applicable."
    )
    port: int | None = Field(None, description="The port number for the service, if applicable.")
    url: str | None = Field(None, description="The full URL for web-based services.")
    raw: str | None = Field(
        None,
        description="The raw connection string or information provided (e.g., 'nc example.com 12345').",
    )
    container: str | None = Field(
        None,
        description="For Docker services, the container image/name.",
    )


class Challenge(BaseModel):
    """Represents a challenge."""

    id: str = Field(
        ...,
        description="The unique identifier of the challenge, typically a number or short string.",
    )
    name: str = Field(..., description="The display name of the challenge.")
    categories: List[str] = Field(
        default_factory=list,
        description="A list of raw categories the challenge belongs to as provided by the platform.",
    )
    normalized_categories: List[str] = Field(
        default_factory=list,
        description="A list of normalized categories (e.g., 'rev' for 'Reverse Engineering').",
    )
    value: int | None = Field(
        None,
        description="The point value awarded for solving the challenge. Can be None if points are dynamic or not applicable.",
    )
    description: str | None = Field(
        None,
        description="The main description, prompt, or story for the challenge. May contain HTML or Markdown.",
    )
    attachments: List[Attachment] = Field(
        default_factory=list,
        description="A list of downloadable files (attachments) associated with the challenge.",
    )
    services: List[Service] = Field(
        default_factory=list,
        description="A list of network services (e.g., netcat listeners, web servers, databases) associated with the challenge.",
    )
    tags: List[str] = Field(
        default_factory=list, description="A list of tags or keywords categorizing the challenge."
    )
    solved: bool | None = Field(
        False,
        description="Indicates if the challenge has been solved by the current user/team. Can be None if status is unknown.",
    )
    authors: List[str] = Field(
        default_factory=list, description="The authors or creators of the challenge."
    )
    difficulty: str | None = Field(
        None,
        description="The perceived difficulty of the challenge (e.g., 'Easy', 'Medium', 'Hard'), if specified.",
    )

    @property
    def category(self) -> str | None:
        """The primary category of the challenge. Returns the first category from the `categories` list, or None if no categories are present."""
        return self.categories[0] if self.categories else None

    @property
    def normalized_category(self) -> str | None:
        """The primary normalized category of the challenge. Returns the first category from the `normalized_categories` list, or None."""
        return self.normalized_categories[0] if self.normalized_categories else None

    @property
    def has_attachments(self) -> bool:
        """Returns True if the challenge has one or more attachments, False otherwise."""
        return bool(self.attachments)

    @property
    def has_services(self) -> bool:
        """Returns True if the challenge has one or more network services, False otherwise."""
        return bool(self.services)

    @property
    def service(self) -> Service | None:
        """Returns the first service."""
        return self.services[0] if self.services else None

    @property
    def author(self) -> str | None:
        """Returns the first author."""
        return self.authors[0] if self.authors else None
