import json
import logging
from typing import Dict

from ctfbridge.base.services.session import SessionHelper
from ctfbridge.exceptions import SessionError

logger = logging.getLogger(__name__)


class CoreSessionHelper(SessionHelper):
    """
    Core implementation of the session helper.
    Provides functionality for managing HTTP session state including headers, cookies, and tokens.
    """

    def __init__(self, client):
        """
        Initialize the session helper.

        Args:
            client: The CTF client instance
        """
        self._client = client

    async def set_token(self, token: str) -> None:
        self._client._http.headers["Authorization"] = f"Bearer {token}"

    async def set_headers(self, headers: Dict[str, str]) -> None:
        self._client._http.headers.update(headers)

    async def set_cookie(self, name: str, value: str, domain: str | None = None) -> None:
        self._client._http.cookies.set(name, value, domain=domain)

    async def save(self, path: str) -> None:
        try:
            cookies_data = []
            for cookie in self._client._http.cookies.jar:
                cookies_data.append(
                    {
                        "name": cookie.name,
                        "value": cookie.value,
                        "domain": cookie.domain,
                    }
                )

            session_state = {
                "headers": dict(self._client._http.headers),
                "cookies": cookies_data,
            }
            with open(path, "w") as f:
                json.dump(session_state, f)
        except Exception as e:
            raise SessionError(path=path, operation="save", reason=str(e)) from e

    async def load(self, path: str) -> None:
        try:
            with open(path) as f:
                session_state = json.load(f)

            self._client._http.headers.update(session_state.get("headers", {}))
            for cookie in session_state.get("cookies", []):
                self._client._http.cookies.set(
                    name=cookie["name"],
                    value=cookie["value"],
                    domain=cookie.get("domain"),
                )
        except FileNotFoundError as e:
            logger.debug("Session load skipped: %s", e)
            raise SessionError(path=path, operation="load", reason="File not found") from e
        except json.JSONDecodeError as e:
            logger.error("Malformed session file at %s", path)
            raise SessionError(path=path, operation="load", reason="Malformed JSON") from e
        except Exception as e:
            logger.debug("Unexpected error during session load")
            raise SessionError(path=path, operation="load", reason=str(e)) from e
