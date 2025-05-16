from ctfbridge.core.services.auth import CoreAuthService
from ctfbridge.models.auth import AuthMethod
from ctfbridge.exceptions import LoginError, TokenAuthError, MissingAuthMethodError
from typing import List
from bs4 import BeautifulSoup, Tag
import logging
from urllib.parse import parse_qs, unquote, urlparse

logger = logging.getLogger(__name__)


class EPTAuthService(CoreAuthService):
    def __init__(self, client):
        self._client = client

    async def get_supported_auth_methods(self) -> List[AuthMethod]:
        return []
