import logging
import re
from typing import Optional, Any
from ctfbridge.platforms.ctfd.http.endpoints import Endpoints

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


async def get_csrf_nonce(client: Any) -> Optional[str]:
    response = await client.get(Endpoints.Misc.BASE_PAGE)
    soup = BeautifulSoup(response.text, "html.parser")
    for script in soup.find_all("script"):
        if script.string and "csrfNonce" in script.string:
            match = re.search(r"'csrfNonce':\s\"([0-9a-f]{64})\"", script.string)
            if match:
                return match.group(1)
    raise ValueError("Missing CSRF token")
