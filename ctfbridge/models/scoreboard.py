from pydantic import BaseModel, Field


class ScoreboardEntry(BaseModel):
    """Represents a single entry (team/user) on the CTF scoreboard."""

    id: str | None = Field(None, description="The ID of the team or user.")
    name: str = Field(..., description="The name of the team or user.")
    score: int = Field(..., description="The total points earned by the team/user.")
    rank: int = Field(..., description="The current position on the scoreboard.")
    total_solves: int | None = Field(
        default=None, description="The total number of challenges solved."
    )
    last_solve_time: str | None = Field(
        default=None, description="Timestamp of the team's/user's most recent solve."
    )
    country_code: str | None = Field(
        default=None, description="Two-letter ISO 3166-1 alpha-2 country code (e.g., 'US', 'KR')."
    )
