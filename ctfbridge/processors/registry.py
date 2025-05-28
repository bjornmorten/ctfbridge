from ctfbridge.parsers.base import BaseChallengeParser

PARSER_REGISTRY: list[type[BaseChallengeParser]] = []


def register_parser(cls: type[BaseChallengeParser]):
    PARSER_REGISTRY.append(cls)
    return cls


def get_all_parsers() -> list[BaseChallengeParser]:
    return [cls() for cls in PARSER_REGISTRY]
