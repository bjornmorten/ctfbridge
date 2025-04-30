import re

from bs4 import BeautifulSoup


def extract_login_nonce(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("input", {"name": "nonce", "type": "hidden"})
    return tag["value"] if tag and tag.has_attr("value") else ""

def extract_csrf_nonce(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for script in soup.find_all("script"):
        if script.string and "csrfNonce" in script.string:
            match = re.search(r"'csrfNonce':\s*\"([a-fA-F0-9]+)\"", script.string)
            if match:
                return match.group(1)
    return ""

