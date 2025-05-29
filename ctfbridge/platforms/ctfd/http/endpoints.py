API_BASE = "/api/v1"


class Endpoints:
    class Auth:
        LOGIN = "/login"
        LOGOUT = "/logout"
        ME = f"{API_BASE}/users/me"

    class Challenges:
        LIST = f"{API_BASE}/challenges"
        SUBMIT = f"{API_BASE}/challenges/attempt"

        @staticmethod
        def detail(id: str) -> str:
            return f"{API_BASE}/challenges/{id}"

    class Scoreboard:
        FULL = f"{API_BASE}/scoreboard"
        TOP_TEAMS = f"{API_BASE}/scoreboard/top"

    class Misc:
        BASE_PAGE = "/"
        SWAGGER = f"{API_BASE}/swagger.json"
