API_BASE = "/api"


class Endpoints:
    class Ctf:
        @staticmethod
        def get_details(ctf_id: int) -> str:
            return f"{API_BASE}/ctfs/{ctf_id}"

    class Challenges:
        CATEGORIES = f"{API_BASE}/public/challenge-categories"

        @staticmethod
        def detail(ctf_id: int, id: int) -> str:
            return f"{API_BASE}/game/{ctf_id}/challenges/{id}"

        SUBMIT_FLAG = f"{API_BASE}/flags/own"

        @staticmethod
        def download_attachment_url(challenge_id: int) -> str:
            return f"{API_BASE}/challenges/{challenge_id}/download"

    class Scoreboard:
        @staticmethod
        def get_scoreboard(ctf_id: int) -> str:
            return f"{API_BASE}/ctfs/scores/{ctf_id}"
