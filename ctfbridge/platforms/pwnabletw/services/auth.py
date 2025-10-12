"""CTFd auth service"""

import logging
from typing import List

from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import LoginError
from ctfbridge.models.auth import AuthMethod
from ctfbridge.platforms.ctfd.http.endpoints import Endpoints
from ctfbridge.platforms.ctfd.utils.csrf import extract_csrf_nonce, get_csrf_nonce

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class PwnableTWAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def _login_with_credentials(self, username: str, password: str) -> None:
        try:
            # Get CSRF token
            resp = await self._client.get("/user/login")
            soup = BeautifulSoup(resp.text, "html.parser")
            csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"}).get("value")
            logger.debug("Got CSRF token %s", csrf_token)

            # Login
            logger.debug("Posting credentials for user %s", username)
            resp = await self._client.post(
                "/user/login",
                data={
                    "csrfmiddlewaretoken": csrf_token,
                    "username": username,
                    "password": password,
                    "next": "",
                },
                headers={"Referer": "https://pwnable.tw/"},
            )

            if "Please enter a correct email and password" in resp.text:
                logger.debug("Incorrect credentials or login denied for user %s", username)
                raise LoginError(username)

            if resp.status_code != 302:
                logger.debug("Unknown response when trying to log in as %s", username)
                raise LoginError(username)

            logger.info("Credential-based login successful for user %s", username)

        except Exception as e:
            logger.debug("Credential-based login failed")
            raise LoginError(username) from e

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        return [AuthMethod.CREDENTIALS]
