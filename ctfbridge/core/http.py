import asyncio
import logging
from importlib.metadata import version
from typing import Any, Callable, Optional

import httpx

from ctfbridge.exceptions import (
    APIError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ServiceUnavailableError,
    UnauthorizedError,
    ValidationError,
)

logger = logging.getLogger("ctfbridge.http")

try:
    __version__ = version("ctfbridge")
except Exception:
    __version__ = "dev"


def extract_error_message(resp: httpx.Response) -> str:
    """
    Extract a human-readable error message from an HTTP response.
    Attempts to parse JSON responses first, falling back to HTTP status reason.

    Args:
        resp: The HTTP response to extract the error message from

    Returns:
        A string containing the error message
    """
    content_type = resp.headers.get("Content-Type", "")
    is_html = "text/html" in content_type or "<html" in resp.text.lower()

    if not is_html and "application/json" in content_type:
        try:
            data = resp.json()
            return data.get("message") or data.get("detail") or data.get("error") or str(data)
        except Exception:
            pass

    return httpx.codes.get_reason_phrase(resp.status_code)


def handle_response(resp: httpx.Response) -> httpx.Response:
    """
    Handle common HTTP response status codes and raise appropriate exceptions.

    Args:
        resp: The HTTP response to handle

    Returns:
        The response if no error was detected

    Raises:
        RateLimitError: When rate limit is exceeded (429)
        ServiceUnavailableError: When service is unavailable (503)
        ServerError: For other 5xx server errors
    """
    status = resp.status_code
    message = extract_error_message(resp)

    if status == 429:
        retry_after = int(resp.headers.get("Retry-After", "0"))
        raise RateLimitError(message or "Rate limit exceeded", retry_after=retry_after)
    elif status == 503:
        raise ServiceUnavailableError(message or "Service unavailable", status_code=status)
    elif 500 <= status < 600:
        raise ServerError(f"Server error ({status}): {message}", status_code=status)
    else:
        return resp


class CTFBridgeClient(httpx.AsyncClient):
    """
    Custom HTTP client for CTFBridge:
    - Automatic global error handling
    - Optional platform-specific postprocessing hook
    - Optional lifecycle hooks: before_request, after_response
    """

    def __init__(
        self,
        postprocess_response: Optional[Callable[[httpx.Response], None]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._postprocess_response = postprocess_response

    async def request(self, method: str, url: str, raw: bool = False, **kwargs) -> httpx.Response:
        logger.debug("Request: %s %s", method, url)
        logger.debug("Request headers: %s", kwargs.get("headers"))
        if "data" in kwargs or "json" in kwargs:
            logger.debug("Request body: %s", kwargs.get("data") or kwargs.get("json"))

        response = await super().request(method, url, **kwargs)

        logger.debug("Response [%s]: %s", response.status_code, response.url)

        if raw:
            return response

        handle_response(response)

        if self._postprocess_response:
            self._postprocess_response(response)

        return response

    def set_postprocess_hook(self, hook: Callable[[httpx.Response], None]):
        self._postprocess_response = hook


def make_http_client(
    *,
    config: dict[str, Any] = {},
) -> CTFBridgeClient:
    """
    Create a preconfigured HTTP client.

    Args:
        config: Dictionary containing httpx client configuration options:
            - timeout: Request timeout in seconds (int/float)
            - retries: Number of retries for failed requests (int)
            - max_connections: Maximum number of concurrent connections (int)
            - http2: Whether to enable HTTP/2 (bool)
            - auth: Authentication credentials (tuple/httpx.Auth)
            - event_hooks: Request/response event hooks (dict)
            - verify_ssl: Whether to verify SSL certificates (bool)
            - headers: Custom HTTP headers (dict)
            - proxy: Proxy configuration (dict/str)
            - user_agent: Custom User-Agent string (str)
    """
    # Extract special configuration options
    max_conns = config.pop("max_connections", 20)
    retries = config.pop("retries", 5)
    user_agent = config.pop("user_agent", f"CTFBridge/{__version__}")
    custom_headers = config.pop("headers", {})

    # Build the final configuration
    client_config = {
        "limits": httpx.Limits(max_connections=max_conns),
        "timeout": config.pop("timeout", 10),
        "verify": config.pop("verify_ssl", True),
        "headers": {"User-Agent": user_agent, **custom_headers},
        "transport": httpx.AsyncHTTPTransport(retries=retries),
        **config,  # Include any remaining config options
    }

    return CTFBridgeClient(**client_config)
