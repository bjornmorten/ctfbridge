API_BASE = "/api/v1"


class Endpoints:
    class Auth:
        LOGIN = f"{API_BASE}/auth/login"

    class Challenges:
        LIST = f"{API_BASE}/challs"

        @staticmethod
        def submit(challenge_id: str) -> str:
            return f"{API_BASE}/challs/{challenge_id}/submit"

    class Users:
        ME = f"{API_BASE}/users/me"

    class Scoreboard:
        NOW = f"{API_BASE}/leaderboard/now"  # Parameterized with limit and offset
