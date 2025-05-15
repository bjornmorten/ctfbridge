import httpx
from importlib.metadata import version

try:
    __version__ = version("ctfbridge")
except Exception:
    __version__ = "dev"


def make_http_client(
    verify_ssl: bool = False, user_agent: str | None = None
) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        limits=httpx.Limits(max_connections=20),
        timeout=10,
        follow_redirects=True,
        verify=verify_ssl,
        headers={
            "User-Agent": user_agent or f"CTFBridge/{__version__}",
        },
        transport=httpx.AsyncHTTPTransport(retries=5),
    )
