from .auto_client import get_client
from .clients.ctfd_client import CTFdClient

__all__ = [
    "CTFdClient",
    "get_client",
]
