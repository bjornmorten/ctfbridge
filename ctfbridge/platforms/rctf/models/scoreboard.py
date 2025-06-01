from typing import List
from pydantic import BaseModel
from ctfbridge.models.scoreboard import ScoreboardEntry


class RCTFScoreboardEntryData(BaseModel):
    id: str
    name: str
    score: int

    def to_core_model(self, rank: int) -> ScoreboardEntry:
        return ScoreboardEntry.model_construct(
            name=self.name,
            score=self.score,
            rank=rank,
        )


class RCTFScoreboardData(BaseModel):
    total: int
    leaderboard: List[RCTFScoreboardEntryData]


class RCTFScoreboardResponse(BaseModel):
    kind: str
    message: str
    data: RCTFScoreboardData
