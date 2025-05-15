from pydantic import BaseModel
from enum import Enum


class AuthMethod(Enum):
    """Auth method"""

    TOKEN = "token"
    CREDENTIALS = "credentials"
    COOKIES = "cookies"


class TokenLoginResponse(BaseModel):
    """Token login response"""

    success: bool
    token: str
