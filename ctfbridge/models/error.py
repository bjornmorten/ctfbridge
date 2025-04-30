from pydantic import BaseModel


class ErrorResponse(BaseModel):
    success: bool
    message: str
