API_BASE = "/api"


class Endpoints:
    class Auth:
        LOGIN = f"{API_BASE}/account/login"

    class Ctf:
        @staticmethod
        def get_details(ctf_id: int) -> str:
            return f"{API_BASE}/game/{ctf_id}/details"

    class Challenges:
        @staticmethod
        def detail(ctf_id: int, id: int) -> str:
            return f"{API_BASE}/game/{ctf_id}/challenges/{id}"

        @staticmethod
        def submit_flag(ctf_id: int, id: int) -> str:
            return f"{API_BASE}/game/{ctf_id}/challenges/{id}"

        @staticmethod
        def get_flag_submission_result(ctf_id: int, id: int, submission_id: str) -> str:
            return f"{API_BASE}/game/{ctf_id}/challenges/{id}/status/{submission_id}"

    class Scoreboard:
        @staticmethod
        def get_scoreboard(ctf_id: int) -> str:
            return f"{API_BASE}/game/{ctf_id}/scoreboard"
