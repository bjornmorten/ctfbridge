import logging
import re
from typing import Optional

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def extract_csrf_nonce(html: str) -> Optional[str]:
    if not html:
        logger.debug("HTML text provided for CSRF extraction was empty.")
        return None

    soup = BeautifulSoup(html, "html.parser")
    for script in soup.find_all("script"):
        if script.string and "csrfNonce" in script.string:
            match = re.search(r"'csrfNonce':\s\"([0-9a-f]{64})\"", script.string)
            if match:
                return match.group(1)

    logger.debug("CSRF nonce not found in the provided HTML.")
    return None
