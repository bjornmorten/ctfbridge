from typing import List, Dict, Any
from pydantic import BaseModel


class RCTFSolve(BaseModel):
    id: str  # Challenge ID
    # other solve details if needed


class RCTFUserProfileData(BaseModel):
    id: str
    name: str
    # teamToken: Optional[str] = None # if present
    solves: List[RCTFSolve] = []
    # Add other user/team fields from /api/v1/users/me
