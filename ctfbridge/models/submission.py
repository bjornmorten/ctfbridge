from pydantic import BaseModel, Field


class SubmissionResult(BaseModel):
    """Represents the result of a flag submission attempt."""

    correct: bool = Field(..., description="Whether the submitted flag was correct.")
    message: str = Field(
        ...,
        description="The response message from the platform (e.g., 'Correct!' or 'Wrong flag').",
    )
