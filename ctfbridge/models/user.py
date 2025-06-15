from pydantic import BaseModel, Field


class User(BaseModel):
    """Represents a user participating in the CTF."""

    id: int = Field(..., description="The unique identifier of the user.")
    name: str = Field(..., description="The username or display name of the user.")
    team_id: int | None = Field(
        default=None, description="The ID of the team the user belongs to, if any."
    )
    score: int | None = Field(
        default=None, description="The user's individual score, if applicable."
    )
    rank: int | None = Field(default=None, description="The user's individual rank, if applicable.")


class Team(BaseModel):
    """Represents a team participating in the CTF."""

    id: int = Field(..., description="The unique identifier of the team.")
    name: str = Field(..., description="The team's display name.")
    score: int = Field(..., description="The team's total score.")
    rank: int = Field(..., description="The team's current position on the scoreboard.")
