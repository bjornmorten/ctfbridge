from typing import Dict
from ctfbridge.base.services.session import SessionHelper
import json
from ctfbridge.exceptions import SessionError


class CoreSessionHelper(SessionHelper):
    def __init__(self, client):
        self._client = client

    async def set_token(self, token: str) -> None:
        self._client._http.headers["Authorization"] = f"Bearer {token}"

    async def set_headers(self, headers: Dict[str, str]) -> None:
        self._client._http.headers.update(headers)

    async def set_cookie(
        self, name: str, value: str, domain: str | None = None
    ) -> None:
        self._client._http.cookies.set(name, value, domain=domain)

    async def save(self, path: str) -> None:
        try:
            session_state = {
                "headers": dict(self._client._http.headers),
                "cookies": self._client._http.cookies.jar.dict(),
            }
            with open(path, "w") as f:
                json.dump(session_state, f)
        except Exception as e:
            raise SessionError(path=path, operation="save", reason=str(e)) from e

    async def load(self, path: str) -> None:
        try:
            with open(path, "r") as f:
                session_state = json.load(f)

            self._client._http.headers.update(session_state.get("headers", {}))

            for name, value in session_state.get("cookies", {}).items():
                self._client._http.cookies.set(name, value)
        except Exception as e:
            raise SessionError(path=path, operation="load", reason=str(e)) from e
