from enum import Enum

from pydantic import BaseModel, Field


class AuthMethod(Enum):
    """Enumeration of supported authentication methods for CTF platforms."""

    TOKEN = "token"  # Authentication using a token
    CREDENTIALS = "credentials"  # Authentication using username/password
    COOKIES = "cookies"  # Authentication using session cookies


class TokenLoginResponse(BaseModel):
    """Response model for token-based authentication."""

    success: bool = Field(..., description="Whether the authentication was successful.")
    token: str = Field(..., description="The authentication token returned by the platform.")
