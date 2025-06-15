from pydantic import BaseModel, Field


class ScoreboardEntry(BaseModel):
    """Represents a single entry (team/user) on the CTF scoreboard."""

    name: str = Field(..., description="The name of the team or user.")
    score: int = Field(..., description="The total points earned by the team/user.")
    rank: int = Field(..., description="The current position on the scoreboard.")
    last_solve_time: str | None = Field(
        default=None, description="Timestamp of the team's/user's most recent solve."
    )
