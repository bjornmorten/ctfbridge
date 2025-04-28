from dataclasses import dataclass, field
from typing import Optional, List, Dict

@dataclass
class Challenge:
    id: int
    name: str
    category: str
    value: int
    description: str
    attachments: List[str] = field(default_factory=list)
    solved: Optional[bool] = False
    extra: Dict[str, any] = field(default_factory=dict)

@dataclass
class SubmissionResult:
    correct: bool
    message: str
