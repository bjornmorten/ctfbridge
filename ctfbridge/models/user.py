from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    team_id: Optional[int] = None
    score: Optional[int] = None
    rank: Optional[int] = None

class Team(BaseModel):
    id: int
    name: str
    score: int
    rank: int

