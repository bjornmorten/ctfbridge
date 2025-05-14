from ctfbridge.platforms.ctfd.client import CTFdClient
from ctfbridge.exceptions import UnknownPlatformError

PLATFORM_CLIENTS = {
    "ctfd": CTFdClient,
}


def get_platform_client(platform_name: str):
    """
    Get the platform client class by name.

    Raises:
        UnknownPlatformError: if the platform is not registered.
    """
    try:
        return PLATFORM_CLIENTS[platform_name]
    except KeyError:
        raise UnknownPlatformError(platform_name)


__all__ = ["PLATFORM_CLIENTS", "get_platform_client"]
