import logging
from typing import List
from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import MissingAuthMethodError
from ctfbridge.models.auth import AuthMethod

logger = logging.getLogger(__name__)


class EPTAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def login(self, *, username: str = "", password: str = "", token: str = "") -> None:
        """
        Login using a user token (from token cookie).
        """
        if not token:
            raise MissingAuthMethodError("EPT only supports token-based login.")

        await self._client.session.set_cookie("token", token)
        logger.info("EPT token set successfully.")

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        return [AuthMethod.TOKEN]
