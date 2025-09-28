API_BASE = "/api"


class Endpoints:
    class Challenges:
        LIST = f"{API_BASE}/challenges"

        @staticmethod
        def submit_flag(id: str) -> str:
            return f"{API_BASE}/challenge/{id}/solve"

        @staticmethod
        def attachment_download(id: str) -> str:
            return f"{API_BASE}/challenge/{id}/file"

    class Misc:
        METADATA = f"{API_BASE}/metadata"
