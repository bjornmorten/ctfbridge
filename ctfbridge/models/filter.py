from typing import List, Optional

from pydantic import BaseModel, Field


class FilterOptions(BaseModel):
    """Represents filtering options for challenge queries."""

    solved: Optional[bool] = Field(
        None, description="Filter by solved status (True for solved, False for unsolved)."
    )
    min_points: Optional[int] = Field(None, description="Minimum point value for challenges.")
    max_points: Optional[int] = Field(None, description="Maximum point value for challenges.")
    category: Optional[str] = Field(None, description="Single category to filter by.")
    categories: Optional[List[str]] = Field(None, description="List of categories to include.")
    tags: Optional[List[str]] = Field(None, description="List of required tags.")
    has_attachments: Optional[bool] = Field(
        None, description="Filter by attachments being present."
    )
    has_services: Optional[bool] = Field(None, description="Filter by services being present.")
    name_contains: Optional[str] = Field(
        None, description="Case-insensitive substring to search in challenge names."
    )
