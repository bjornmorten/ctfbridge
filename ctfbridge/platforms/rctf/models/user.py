from typing import List, Optional

from pydantic import BaseModel


class RCTFSolve(BaseModel):
    id: str
    name: str
    category: str
    points: int
    solves: int
    createdAt: Optional[int] = None


class RCTFUserProfileData(BaseModel):
    id: str
    name: str
    email: str
    division: str
    ctftimeId: Optional[int] = None
    score: int
    globalPlace: Optional[int] = None
    divisionPlace: Optional[int] = None
    solves: List[RCTFSolve]
    teamToken: str
    allowedDivisions: List[str]

    def has_solved(self, challenge_id: str) -> bool:
        return any(s.id == challenge_id for s in self.solves)
