import importlib
from typing import Any, Type

# Maps platform names to their client class paths
PLATFORM_CLIENTS: dict[str, str] = {
    "ctfd": "ctfbridge.platforms.ctfd.client.CTFdClient",
    "rctf": "ctfbridge.platforms.rctf.client.RCTFClient",
    "berg": "ctfbridge.platforms.berg.client.BergClient",
    "ept": "ctfbridge.platforms.ept.client.EPTClient",
    "gzctf": "ctfbridge.platforms.gzctf.client.GZCTFClient",
    "htb": "ctfbridge.platforms.htb.client.HTBClient",
    "cryptohack": "ctfbridge.platforms.cryptohack.client.CryptoHackClient",
    "pwnabletw": "ctfbridge.platforms.pwnabletw.client.PwnableTWClient",
    "pwnablekr": "ctfbridge.platforms.pwnablekr.client.PwnableKRClient",
    "pwnablexyz": "ctfbridge.platforms.pwnablexyz.client.PwnableXYZClient",
    "pwncollege": "ctfbridge.platforms.pwncollege.client.PwnCollegeClient",
}

# Maps platform names to their identifier class paths
PLATFORM_IDENTIFIERS: dict[str, str] = {
    "ctfd": "ctfbridge.platforms.ctfd.identifier.CTFdIdentifier",
    "rctf": "ctfbridge.platforms.rctf.identifier.RCTFIdentifier",
    "berg": "ctfbridge.platforms.berg.identifier.BergIdentifier",
    "ept": "ctfbridge.platforms.ept.identifier.EPTIdentifier",
    "gzctf": "ctfbridge.platforms.gzctf.identifier.GZCTFIdentifier",
    "htb": "ctfbridge.platforms.htb.identifier.HTBIdentifier",
    "cryptohack": "ctfbridge.platforms.cryptohack.identifier.CryptoHackIdentifier",
    "pwnabletw": "ctfbridge.platforms.pwnabletw.identifier.PwnableTWIdentifier",
    "pwnablekr": "ctfbridge.platforms.pwnablekr.identifier.PwnableKRIdentifier",
    "pwnablexyz": "ctfbridge.platforms.pwnablexyz.identifier.PwnableXYZIdentifier",
    "pwncollege": "ctfbridge.platforms.pwncollege.identifier.PwnCollegeIdentifier",
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
