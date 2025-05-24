from typing import List, Optional

from pydantic import BaseModel


class FilterOptions(BaseModel):
    solved: Optional[bool] = None
    min_points: Optional[int] = None
    max_points: Optional[int] = None
    category: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    name_contains: Optional[str] = None
    enrich: bool = True
