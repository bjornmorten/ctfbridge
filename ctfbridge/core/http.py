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
        raise RateLimitError(message or "Rate limit exceeded", retry_after=retry_after)
    elif 500 <= status < 600:
        raise ServerError(f"Server error ({status}): {message}", status_code=status)
    elif status == 503:
        raise ServiceUnavailableError(message or "Service unavailable", status_code=status)
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
        before_request: Optional[Callable[[str, str, dict], None]] = None,
        after_response: Optional[Callable[[httpx.Response], None]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._postprocess_response = postprocess_response
        self._before_request = before_request
        self._after_response = after_response

    async def request(self, method: str, url: str, raw: bool = False, **kwargs) -> httpx.Response:
        if self._before_request:
            self._before_request(method, url, kwargs)

        logger.debug("Request: %s %s", method, url)
        logger.debug("Request headers: %s", kwargs.get("headers"))
        if "data" in kwargs or "json" in kwargs:
            logger.debug("Request body: %s", kwargs.get("data") or kwargs.get("json"))

        response = await super().request(method, url, **kwargs)

        logger.debug("Response [%s]: %s", response.status_code, response.url)

        if self._after_response:
            self._after_response(response)

        if raw:
            return response

        handle_response(response)

        if self._postprocess_response:
            self._postprocess_response(response)

        return response

    def set_postprocess_hook(self, hook: Callable[[httpx.Response], None]):
        self._postprocess_response = hook

    def set_before_request_hook(self, hook: Callable[[str, str, dict], None]):
        self._before_request = hook

    def set_after_response_hook(self, hook: Callable[[httpx.Response], None]):
        self._after_response = hook


def make_http_client(
    verify_ssl: bool = False,
    user_agent: Optional[str] = None,
) -> CTFBridgeClient:
    """
    Create a preconfigured HTTP client.
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
