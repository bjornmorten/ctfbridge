from pydantic import BaseModel

from ctfbridge.models.scoreboard import ScoreboardEntry


class HTBScoreboardEntry(BaseModel):
    id: int
    name: str
    points: int
    rank: int
    owned_flags: int
    country_code: str

    def to_core_model(self) -> ScoreboardEntry:
        return ScoreboardEntry.model_construct(
            id=str(self.id),
            name=self.name,
            score=self.points,
            rank=self.rank,
            total_solves=self.owned_flags,
            country_code=self.country_code,
        )
