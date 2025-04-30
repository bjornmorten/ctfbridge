from ctfbridge.exceptions import LoginError
from ctfbridge.services import AuthService


class DemoAuthService(AuthService):
    """
    Base authentication service.
    """
    def __init__(self, client):
        super().__init__(client)

    def login(self, username: str = '', password: str = '', token: str = '') -> None:
        if username == "demo" and password == "demo":
            self.client.logged_in = True
        else:
            raise LoginError("Incorrect username or password.")

    def logout(self):
        self.client.logged_in = False