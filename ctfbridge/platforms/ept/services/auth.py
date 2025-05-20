import logging
from typing import List
from urllib.parse import parse_qs, unquote, urlparse

from bs4 import BeautifulSoup, Tag

from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.exceptions import LoginError, MissingAuthMethodError, TokenAuthError
from ctfbridge.models.auth import AuthMethod

logger = logging.getLogger(__name__)


class EPTAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        return []
