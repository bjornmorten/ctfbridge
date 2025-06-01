class Endpoints:
    """
    Centralized API endpoints for the HTB platform.
    Paths are relative to the global HTB API base URL.
    """

    class Ctf:
        """Endpoints related to specific CTF events."""

        @staticmethod
        def detail(ctf_id: str) -> str:
            """Gets details for a specific CTF event (challenges, etc.)."""
            return f"ctfs/{ctf_id}"

        @staticmethod
        def scores(ctf_id: str) -> str:
            """Gets the scoreboard for a specific CTF event."""
            return f"ctfs/scores/{ctf_id}"

    class Challenges:
        """Endpoints related to challenges."""

        @staticmethod
        def download(challenge_id: str) -> str:
            """Gets the download link for a challenge attachment."""
            return f"challenges/{challenge_id}/download"

        CATEGORIES = "public/challenge-categories"
        """Gets all available challenge categories."""

    class Flags:
        """Endpoints related to flag submissions."""

        SUBMIT = "flags/own"
        """Submits a flag for a challenge."""
