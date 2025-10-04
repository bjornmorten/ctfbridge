import importlib
from typing import Any, Type

# Maps platform names to their client class paths
PLATFORM_CLIENTS: dict[str, str] = {
    "ctfd": "ctfbridge.platforms.ctfd.client.CTFdClient",
    "rctf": "ctfbridge.platforms.rctf.client.RCTFClient",
    "berg": "ctfbridge.platforms.berg.client.BergClient",
    "ept": "ctfbridge.platforms.ept.client.EPTClient",
    "gzctf": "ctfbridge.platforms.gzctf.client.GZCTFClient",
}

# Maps platform names to their identifier class paths
PLATFORM_IDENTIFIERS: dict[str, str] = {
    "ctfd": "ctfbridge.platforms.ctfd.identifier.CTFdIdentifier",
    "rctf": "ctfbridge.platforms.rctf.identifier.RCTFIdentifier",
    "berg": "ctfbridge.platforms.berg.identifier.BergIdentifier",
    "ept": "ctfbridge.platforms.ept.identifier.EPTIdentifier",
    "gzctf": "ctfbridge.platforms.gzctf.identifier.GZCTFIdentifier",
}


def import_object(dotted_path: str) -> Any:
    """Import a class or function by dotted path."""
    module_path, object_name = dotted_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def get_platform_client(name: str) -> type:
    """Lazily return the platform client class."""
    if name not in PLATFORM_CLIENTS:
        raise ValueError(f"Unknown platform: {name}")
    return import_object(PLATFORM_CLIENTS[name])


def get_identifier_classes() -> list[tuple[str, Type]]:
    return [(name, import_object(path)) for name, path in PLATFORM_IDENTIFIERS.items()]
