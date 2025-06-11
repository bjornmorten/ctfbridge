import httpx


class CTFdSeeder:
    """Uses the CTFd API to seed a fresh instance with test data."""

    def __init__(self, base_url: str, admin_pass: str = "password"):
        self.base_url = base_url
        self.admin_pass = admin_pass
        self.client = httpx.Client()

    def init_instance(self):
        """Initialises the CTFd instance."""
        pass

    def create_user(self, name: str, password: str, email: str):
        """Creates a user."""
        pass

    def create_challenge(self, name: str, category: str, description: str, value: int, flag: str):
        """Creates a new challenge."""
        pass

    def run_seed(self):
        """Executes the full seeding process."""
        print(f"Starting to seed CTFd instance at {self.base_url}")
        self.init_platform()
        self.create_user(name="test", password="password", email="test@user.com")
        self.create_challenge(
            name="Test Challenge",
            category="Test",
            description="A test challenge.",
            value=1337,
            flag="CTF{seeded_flag}",
        )
        print("Seeding complete.")
