import logging

from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import LoginError
from ctfbridge.models.auth import AuthMethod

logger = logging.getLogger(__name__)


def is_jwt_like(token: str) -> bool:
    parts = token.split(".")
    if len(parts) != 3:
        return False
    return all(parts)


class HTBAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def _login_with_token(self, token: str) -> None:
        if not is_jwt_like(token):
            raise LoginError("Provided token does not look like a JWT.")

        await self._client.session.set_token(token)

    async def get_supported_auth_methods(self) -> list[AuthMethod]:
        return [AuthMethod.TOKEN]
