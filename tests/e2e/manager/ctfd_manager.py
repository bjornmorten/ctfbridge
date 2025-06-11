import httpx
from bs4 import BeautifulSoup


class CTFdManager:
    def __init__(self, base_url: str, admin_pass: str = "password"):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(follow_redirects=True)
        self.admin_token: str | None = None

    # ────────────────────────────  Bootstrapping  ────────────────────────────── #

    def init_instance(self) -> None:
        """Run the /setup wizard programmatically"""
        nonce = self._get_nonce("/setup")

        form = {
            "ctf_name": "Seeded CTF",
            "ctf_description": "Seeded for automated tests",
            "user_mode": "users",
            "challenge_visibility": "private",
            "account_visibility": "public",
            "score_visibility": "public",
            "registration_visibility": "public",
            "verify_emails": "false",
            "team_size": "",
            "name": "admin",
            "email": "admin@ctfd.local",
            "password": "admin",
            # empty file inputs
            "ctf_logo": ("", b"", "application/octet-stream"),
            "ctf_banner": ("", b"", "application/octet-stream"),
            "ctf_small_icon": ("", b"", "application/octet-stream"),
            "ctf_theme": "core-beta",
            "theme_color": "",
            "start": "",
            "end": "",
            "_submit": "Finish",
            "nonce": nonce,
        }
        files = {k: v if isinstance(v, tuple) else (None, v) for k, v in form.items()}
        self.client.post(f"{self.base_url}/setup", files=files).raise_for_status()

        # self._login_admin()

    def _login_admin(self) -> None:
        """Store an API token for subsequent requests."""
        self.client.post(
            f"{self.base_url}/login", data={"name": "admin", "password": "admin"}
        ).raise_for_status()

        resp = self.client.get(f"{self.base_url}/api/v1/tokens/me").raise_for_status()
        self.admin_token = resp.json()["data"]["token"]
        self.client.headers.update({"Authorization": f"Token {self.admin_token}"})

    # ────────────────────────────  Seeding  ─────────────────────────────────── #

    def create_user(self, name: str, password: str, email: str) -> None:
        self.client.post(
            f"{self.base_url}/api/v1/users",
            json={"name": name, "email": email, "password": password},
        ).raise_for_status()

    def create_challenge(
        self,
        name: str,
        category: str,
        description: str,
        value: int,
        flag: str,
        state: str = "visible",
    ) -> None:
        chall = (
            self.client.post(
                f"{self.base_url}/api/v1/challenges",
                json={
                    "name": name,
                    "category": category,
                    "description": description,
                    "value": value,
                    "type": "standard",
                    "state": state,
                },
            )
            .raise_for_status()
            .json()["data"]
        )

        self.client.post(
            f"{self.base_url}/api/v1/flags",
            json={
                "challenge_id": chall["id"],
                "type": "static",
                "content": flag,
            },
        ).raise_for_status()

    # ────────────────────────────  Runtime Control  ─────────────────────────── #

    def update_ctf_setting(self, key: str, value: str) -> None:
        self.client.patch(f"{self.base_url}/api/v1/configs", json={key: value}).raise_for_status()

    def toggle_challenge_visibility(self, visibility: str) -> None:
        """visibility ∈ {'hidden','private','public'}"""
        self.update_ctf_setting("challenge_visibility", visibility)

    # ────────────────────────────  Helpers  ─────────────────────────────────── #

    def _get_nonce(self, path: str) -> str:
        html = self.client.get(f"{self.base_url}{path}").text
        tag = BeautifulSoup(html, "html.parser").find("input", {"name": "nonce"})
        if not tag:
            raise RuntimeError("CSRF nonce not found on page %s" % path)
        return tag["value"]

    # ────────────────────────────  Convenience  ─────────────────────────────── #

    def run_seed(self) -> None:
        """Opinionated all-in-one seeding used by seed_main.py."""
        print(f"Seeding CTFd instance at {self.base_url} …")
        self.init_instance()
        """
        self.create_user("test", "password", "test@user.com")
        self.create_challenge(
            name="Test Challenge",
            category="Test",
            description="A test challenge.",
            value=1337,
            flag="CTF{seeded_flag}",
        )
        """
        print("Seed complete ✅")
