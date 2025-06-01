from pydantic import BaseModel
from ctfbridge.models.submission import SubmissionResult


class RCTFSubmissionResponse(BaseModel):
    kind: str
    message: str

    def to_core_model(self) -> SubmissionResult:
        return SubmissionResult(
            correct=self.kind == "goodFlag" or self.kind == "badAlreadySolvedChallenge",
            message=self.message,
        )
