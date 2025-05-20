from enum import Enum

from pydantic import BaseModel


class AuthMethod(Enum):
    """Auth method"""

    TOKEN = "token"
    CREDENTIALS = "credentials"
    COOKIES = "cookies"


class TokenLoginResponse(BaseModel):
    """Token login response"""

    success: bool
    token: str
