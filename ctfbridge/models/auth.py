from pydantic import BaseModel


class TokenLoginResponse(BaseModel):
    success: bool
    token: str

