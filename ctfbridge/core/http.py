import httpx
from importlib.metadata import version

from ctfbridge.exceptions import (
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    ValidationError,
    RateLimitError,
    ServerError,
    ServiceUnavailableError,
)

try:
    __version__ = version("ctfbridge")
except Exception:
    __version__ = "dev"


def extract_error_message(resp: httpx.Response) -> str:
    """
    Extract a clean, meaningful error message from the response.
    Falls back to standard status phrases if the content is HTML.
    """
    content_type = resp.headers.get("Content-Type", "")
    is_html = "text/html" in content_type or "<html" in resp.text.lower()

    if not is_html and "application/json" in content_type:
        try:
            data = resp.json()
            return (
                data.get("message")
                or data.get("detail")
                or data.get("error")
                or str(data)
            )
        except Exception:
            pass

    return httpx.codes.get_reason_phrase(resp.status_code)


def handle_response(resp: httpx.Response):
    """
    Raise appropriate exceptions based on HTTP status codes.
    Return parsed data for success responses.
    """
    status = resp.status_code
    message = extract_error_message(resp)

    if status == 400:
        raise BadRequestError(message, status_code=status)
    elif status == 401:
        raise UnauthorizedError(message or "Unauthorized", status_code=status)
    elif status == 403:
        raise ForbiddenError(message or "Forbidden", status_code=status)
    elif status == 404:
        raise NotFoundError(message or "Not found", status_code=status)
    elif status == 409:
        raise ConflictError(message or "Conflict", status_code=status)
    elif status == 422:
        raise ValidationError(message or "Unprocessable entity", status_code=status)
    elif status == 429:
        retry_after = int(resp.headers.get("Retry-After", "0"))
        raise RateLimitError(retry_after=retry_after)
    elif 500 <= status < 600:
        raise ServerError(f"Server error ({status}): {message}", status_code=status)
    elif status == 503:
        raise ServiceUnavailableError(
            message or "Service unavailable", status_code=status
        )
    elif status in (200, 201):
        return resp
    elif status == 204:
        return None
    else:
        # Fallback for unknown status codes
        resp.raise_for_status()


class CTFBridgeClient(httpx.AsyncClient):
    """
    Custom HTTP client that automatically handles API errors using handle_response().
    """

    async def request(self, method: str, url: str, **kwargs):
        response = await super().request(method, url, **kwargs)
        return handle_response(response)


def make_http_client(
    verify_ssl: bool = False, user_agent: str | None = None
) -> CTFBridgeClient:
    """
    Create a preconfigured HTTP client for CTFBridge with automatic error handling.
    """
    return CTFBridgeClient(
        limits=httpx.Limits(max_connections=20),
        timeout=10,
        follow_redirects=True,
        verify=verify_ssl,
        headers={
            "User-Agent": user_agent or f"CTFBridge/{__version__}",
        },
        transport=httpx.AsyncHTTPTransport(retries=5),
    )
