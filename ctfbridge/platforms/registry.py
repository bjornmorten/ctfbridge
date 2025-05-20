from ctfbridge.base.client import CTFClient
from ctfbridge.base.identifier import PlatformIdentifier
from ctfbridge.exceptions import UnknownPlatformError

IDENTIFIER_REGISTRY: dict[str, type[PlatformIdentifier]] = {}
PLATFORM_CLIENTS: dict[str, type[CTFClient]] = {}


# Identifier
def register_identifier(name: str):
    def decorator(cls: type[PlatformIdentifier]):
        if name in IDENTIFIER_REGISTRY:
            raise ValueError(f"Identifier '{name}' already registered.")
        IDENTIFIER_REGISTRY[name] = cls
        return cls

    return decorator


def get_all_identifiers() -> list[tuple[str, type[PlatformIdentifier]]]:
    return list(IDENTIFIER_REGISTRY.items())


# Platform
def platform(name: str):
    def wrapper(cls: type[CTFClient]):
        if name in PLATFORM_CLIENTS:
            raise ValueError(f"Platform '{name}' already registered.")
        PLATFORM_CLIENTS[name] = cls
        return cls

    return wrapper


def get_platform_client(name: str):
    try:
        return PLATFORM_CLIENTS[name]
    except KeyError as e:
        raise UnknownPlatformError(name) from e
