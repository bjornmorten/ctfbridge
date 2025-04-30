from ctfbridge.exceptions import LoginError
from ctfbridge.services import AuthService

from ..utils import extract_login_nonce


class CTFdAuthService(AuthService):
    """
    Base authentication service.
    """
    def __init__(self, client):
        super().__init__(client)

    def login(self, username: str = '', password: str = '', token: str = '') -> None:
        session = self.client.session
        base_url = self.client.base_url

        # Step 1: Get nonce from login page
        resp = session.get(f"{base_url}/login")
        nonce = extract_login_nonce(resp.text)
        if not nonce:
            raise LoginError("Failed to extract CSRF token for login.")

        # Step 2: Post credentials
        resp = session.post(
            f"{base_url}/login",
            data={"name": username, "password": password, "nonce": nonce}
        )

        if "incorrect" in resp.text.lower():
            raise LoginError("Incorrect username or password.")