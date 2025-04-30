from ctfbridge.exceptions import LoginError
from ctfbridge.services import AuthService
from urllib.parse import unquote

from ..utils import extract_token_from_url

class RCTFAuthService(AuthService):
    """
    Base authentication service.
    """
    def __init__(self, client):
        super().__init__(client)

    def login(self, username: str = '', password: str = '', token: str = '') -> None:
        if not token:
            raise ValueError("You must provide a team token for rCTF login.")                                                                                 
        if token.startswith("http"):
            token = extract_token_from_url(token)
        else:
            token = unquote(token)

        url = f"{self.client.base_url}/api/v1/auth/login"
        payload = {"teamToken": token}

        response = self.client.session.post(url, json=payload)
        response.raise_for_status()

        result = response.json()
        if result["kind"] != "goodLogin":
            raise LoginError("Login failed: Unexpected server response.")

        auth_token = result["data"]["authToken"]
        self.client.set_token(auth_token)