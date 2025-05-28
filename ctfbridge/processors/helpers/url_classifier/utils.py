from dataclasses import dataclass
from urllib.parse import ParseResult


@dataclass
class LinkClassifierContext:
    link: str
    parsed: ParseResult
