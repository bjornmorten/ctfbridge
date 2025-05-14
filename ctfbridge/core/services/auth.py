from ctfbridge.base.services.auth import AuthService


class CoreAuthService(AuthService):
    def __init__(self, client):
        self._client = client

    async def logout(self):
        self._client.http.cookies.clear()
        self._client.http.session.headers.pop("Authorization", None)
