from pydantic import BaseModel


class SubmissionResult(BaseModel):
    correct: bool
    message: str
