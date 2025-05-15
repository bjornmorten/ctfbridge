from urllib.parse import ParseResult
from dataclasses import dataclass


@dataclass
class LinkClassifierContext:
    link: str
    parsed: ParseResult
