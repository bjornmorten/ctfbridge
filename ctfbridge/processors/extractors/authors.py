import re

from ctfbridge.models.challenge import Challenge
from ctfbridge.processors.base import BaseChallengeParser
from ctfbridge.processors.registry import register_parser


@register_parser
class AuthorExtractor(BaseChallengeParser):
    def apply(self, challenge: Challenge) -> Challenge:
        if challenge.author or not challenge.description:
            return challenge

        match = re.search(r"(?i)author\s*[:\-]\s*(\w+)", challenge.description)
        if match:
            challenge.author = match.group(1)
        return challenge
