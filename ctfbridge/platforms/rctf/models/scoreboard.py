from pydantic import BaseModel
from ctfbridge.models.scoreboard import ScoreboardEntry


class RCTFScoreboardEntryData(BaseModel):
    name: str
    score: int
    # Add other fields rCTF provides, e.g., user_id, last_solve_time
    # You will also need the rank from the iteration, not from the object itself usually

    def to_core_model(self, rank: int) -> ScoreboardEntry:
        return ScoreboardEntry.model_construct(
            name=self.name,
            score=self.score,
            rank=rank,
        )
