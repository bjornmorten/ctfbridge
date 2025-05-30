import logging
from functools import wraps
from typing import List, Type

from ctfbridge.processors.base import BaseChallengeParser

logger = logging.getLogger(__name__)

PARSER_REGISTRY: List[Type[BaseChallengeParser]] = []


def register_parser(cls: Type[BaseChallengeParser]) -> Type[BaseChallengeParser]:
    """Register a challenge parser.

    Args:
        cls: The parser class to register.

    Returns:
        The registered parser class.

    Raises:
        TypeError: If the class doesn't inherit from BaseChallengeParser.
    """
    if not issubclass(cls, BaseChallengeParser):
        raise TypeError(f"Parser {cls.__name__} must inherit from BaseChallengeParser")

    if cls in PARSER_REGISTRY:
        logger.debug(f"Parser {cls.__name__} is already registered")
        return cls

    logger.debug(f"Registering parser: {cls.__name__}")
    PARSER_REGISTRY.append(cls)
    return cls


def get_all_parsers() -> List[BaseChallengeParser]:
    """Get instances of all registered parsers.

    Returns:
        A list of instantiated parser objects.
    """
    parsers = []
    for cls in PARSER_REGISTRY:
        try:
            parser = cls()
            parsers.append(parser)
        except Exception as e:
            logger.error(f"Failed to instantiate parser {cls.__name__}: {e}")
    return parsers


def clear_registry() -> None:
    """Clear all registered parsers. Mainly used for testing."""
    PARSER_REGISTRY.clear()
