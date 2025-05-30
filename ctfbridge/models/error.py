from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Represents an error response from the CTF platform."""

    success: bool = Field(..., description="Always False for error responses.")
    message: str = Field(..., description="The error message describing what went wrong.")
