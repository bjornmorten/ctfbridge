from ctfbridge.factory import create_client
from importlib.metadata import version

try:
    __version__ = version("ctfbridge")
except Exception:
    __version__ = "dev"

__all__ = ["create_client", "__version__"]
