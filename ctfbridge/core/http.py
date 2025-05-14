import httpx
from ctfbridge import __version__
import asyncio


def make_http_client(
    verify_ssl: bool = True, user_agent: str | None = None
) -> httpx.AsyncClient:
    transport = httpx.AsyncHTTPTransport(retries=3)
    return httpx.AsyncClient(
        timeout=httpx.Timeout(5.0),
        follow_redirects=True,
        verify=verify_ssl,
        headers={
            "User-Agent": f"CTFBridge/{__version__}",
        },
        transport=transport,
    )
