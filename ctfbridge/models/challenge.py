from enum import Enum

from pydantic import (
    BaseModel,
    Field,
    computed_field,
    field_validator,
    model_serializer,
    field_serializer,
)
from pydantic.config import ConfigDict


class ServiceType(str, Enum):
    """Enumeration of possible service types for CTF challenges."""

    TCP = "tcp"
    UDP = "udp"
    HTTP = "http"
    SSH = "ssh"
    FTP = "ftp"
    TELNET = "telnet"


class DownloadType(str, Enum):
    HTTP = "http"
    SSH = "ssh"


class DownloadInfo(BaseModel):
    """Describes how to obtain an attachment."""

    type: DownloadType = Field(DownloadType.HTTP, description="How to access the resource.")
    url: str | None = Field(None, description="Direct download URL if applicable.")
    host: str | None = Field(None, description="Hostname for SSH or other remote connections.")
    port: int | None = Field(None, description="Port number for remote access.")
    path: str | None = Field(None, description="Path to the resource on the remote system.")
    username: str | None = Field(None, description="Username if required for SSH or API.")
    password: str | None = Field(None, description="Password or token, if available.")
    key: str | None = Field(None, description="Key, if available.")
    extra: dict[str, str] | None = Field(
        default_factory=dict,
        description="Additional platform-specific metadata.",
    )


class Attachment(BaseModel):
    """Represents a downloadable attachment file for a challenge."""

    name: str | None = Field(None, description="The display name of the attachment file, if known.")
    local_path: str | None = Field(
        None, description="Local file path after download, if available."
    )
    size_bytes: int | None = Field(None, description="Size of the file in bytes, if known.")
    download_info: DownloadInfo = Field(None, description="How to obtain this attachment.")

    @computed_field
    @property
    def is_pending(self) -> bool:
        """True if no metadata is known yet."""
        return self.name is None


class AttachmentState(str, Enum):
    NONE = "none"
    KNOWN = "known"
    PENDING = "pending"
    PARTIAL = "partial"


class AttachmentCollection(BaseModel):
    """Unified collection of all attachments (fetched or not)."""

    attachments: list[Attachment] = Field(default_factory=list)

    def __iter__(self):
        return iter(self.attachments)

    def __len__(self):
        return len(self.attachments)

    def __getitem__(self, index):
        return self.attachments[index]

    def __bool__(self):
        return bool(self.attachments)

    @computed_field
    @property
    def state(self) -> AttachmentState:
        if not self.attachments:
            return AttachmentState.NONE

        pending = [a.is_pending for a in self.attachments]

        if all(pending):
            return AttachmentState.PENDING
        elif any(pending):
            return AttachmentState.PARTIAL
        else:
            return AttachmentState.KNOWN

    @computed_field
    @property
    def is_unfetched(self) -> bool:
        """True if at least one attachment hasn't been fetched yet."""
        return any(a.is_pending for a in self.attachments)

    @model_serializer
    def serialize_as_list(self):
        """Serialize as just a list of attachments."""
        return self.attachments


class ProgressData(BaseModel):
    """Represents the state of an ongoing attachment download."""

    attachment: Attachment = Field(..., description="The attachment being downloaded.")
    downloaded_bytes: int = Field(..., description="The number of bytes downloaded so far.")
    total_bytes: int = Field(..., description="The total size of the attachment in bytes.")
    percentage: float = Field(
        ..., ge=0, le=100, description="The download progress as a percentage."
    )
    speed_bps: float = Field(..., description="The current download speed in bytes per second.")
    eta_seconds: float | None = Field(None, description="The estimated time remaining in seconds.")


class Service(BaseModel):
    """Describes a network service associated with a challenge (e.g., nc host port, http URL)."""

    type: ServiceType = Field(..., description="The type of the network service (e.g., tcp, http).")
    host: str | None = Field(
        default=None, description="The hostname or IP address of the service, if applicable."
    )
    port: int | None = Field(
        default=None, description="The port number for the service, if applicable."
    )
    url: str | None = Field(default=None, description="The full URL for web-based services.")
    raw: str | None = Field(
        default=None,
        description="The raw connection string or information provided (e.g., 'nc example.com 12345').",
    )


class Challenge(BaseModel):
    """Represents a challenge."""

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(
        ...,
        description="The unique identifier of the challenge, typically a number or short string.",
    )
    name: str = Field(..., description="The display name of the challenge.")
    categories: list[str] = Field(
        default_factory=list,
        description="A list of raw categories the challenge belongs to as provided by the platform.",
    )
    normalized_categories: list[str] = Field(
        default_factory=list,
        description="A list of normalized categories (e.g., 'rev' for 'Reverse Engineering').",
    )
    subcategory: str | None = Field(
        default=None,
        description="A more specific category under the main category, if the platform defines one.",
    )
    value: int | None = Field(
        default=None,
        description="The point value awarded for solving the challenge. Can be None if points are dynamic or not applicable.",
    )
    description: str | None = Field(
        default=None,
        description="The main description, prompt, or story for the challenge. May contain HTML or Markdown.",
    )
    attachments: AttachmentCollection = Field(
        default_factory=AttachmentCollection,
        description="A collection of downloadable files associated with the challenge.",
    )
    services: list[Service] = Field(
        default_factory=list,
        description="A list of network services (e.g., netcat listeners, web servers, databases) associated with the challenge.",
    )
    tags: list[str] = Field(
        default_factory=list, description="A list of tags or keywords categorizing the challenge."
    )
    solved: bool | None = Field(
        default=False,
        description="Indicates if the challenge has been solved by the current user/team. Can be None if status is unknown.",
    )
    authors: list[str] = Field(
        default_factory=list, description="The authors or creators of the challenge."
    )
    difficulty: str | None = Field(
        default=None,
        description="The perceived difficulty of the challenge (e.g., 'Easy', 'Medium', 'Hard'), if specified.",
    )
    flag_format: str | None = Field(
        default=None,
        description="The flag format of the challenge.",
    )

    @computed_field
    @property
    def category(self) -> str | None:
        """The primary category of the challenge. Returns the first category from the `categories` list, or None if no categories are present."""
        return self.categories[0] if self.categories else None

    @computed_field
    @property
    def normalized_category(self) -> str | None:
        """The primary normalized category of the challenge. Returns the first category from the `normalized_categories` list, or None."""
        return self.normalized_categories[0] if self.normalized_categories else None

    @computed_field
    @property
    def has_attachments(self) -> bool:
        """Returns True if the challenge has one or more attachments, False otherwise."""
        return bool(self.attachments)

    @computed_field
    @property
    def has_services(self) -> bool:
        """Returns True if the challenge has one or more network services, False otherwise."""
        return bool(self.services)

    @computed_field
    @property
    def service(self) -> Service | None:
        """Returns the first service."""
        return self.services[0] if self.services else None

    @computed_field
    @property
    def author(self) -> str | None:
        """Returns the first author."""
        return self.authors[0] if self.authors else None

    @field_serializer("attachments")
    def serialize_attachments(self, attachments: AttachmentCollection):
        return attachments.model_dump()


class FilterOptions(BaseModel):
    """
    Filtering parameters used to retrieve specific challenges.
    """

    solved: bool | None = Field(
        default=None,
        description="If True, only solved; if False, only unsolved; if None, no filter.",
    )
    min_points: int | None = Field(
        default=None,
        description="Minimum point value a challenge must have.",
    )
    max_points: int | None = Field(
        default=None,
        description="Maximum point value a challenge can have.",
    )
    category: str | None = Field(
        default=None,
        description="Only include challenges from this specific category.",
    )
    categories: list[str] | None = Field(
        default=None,
        description="Only include challenges from any of these categories.",
    )
    tags: list[str] | None = Field(
        default=None,
        description="Only include challenges that have all of these tags.",
    )
    has_attachments: bool | None = Field(
        default=None,
        description="Filter by whether challenges have attachments.",
    )
    has_services: bool | None = Field(
        default=None,
        description="Filter by whether challenges have services.",
    )
    name_contains: str | None = Field(
        default=None,
        description="Filter by whether challenge name contains this substring.",
    )
