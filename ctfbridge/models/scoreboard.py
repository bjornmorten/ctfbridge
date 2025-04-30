from typing import Optional

from pydantic import BaseModel


class ScoreboardEntry(BaseModel):
    name: str
    score: int
    rank: int
    last_solve_time: Optional[str] = None

