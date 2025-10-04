from pydantic import BaseModel

from ctfbridge.models.scoreboard import ScoreboardEntry


class GZCTFScoreboardEntry(BaseModel):
    name: str
    score: int
    rank: int

    def to_core_model(self) -> ScoreboardEntry:
        return ScoreboardEntry.model_construct(name=self.name, score=self.score, rank=self.rank)
