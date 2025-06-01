"""Models for CTFd scoreboard data"""

from pydantic import BaseModel

from ctfbridge.models.scoreboard import ScoreboardEntry


class CTFdScoreboardEntry(BaseModel):
    """Model for CTFd scoreboard entry"""

    name: str
    score: int
    pos: int

    def to_core_model(self) -> ScoreboardEntry:
        """Convert to core ScoreboardEntry model"""
        return ScoreboardEntry.model_construct(name=self.name, score=self.score, rank=self.pos)
