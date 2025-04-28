import time
import requests
from ..utils.response_checker import check_response_valid
from ..exceptions import RateLimitError

class ValidatedSession(requests.Session):
    """Session that automatically checks response validity (session expiration, rate limits)."""

    def __init__(self, max_retries: int = 5):
        super().__init__()
        self.max_retries = max_retries

    def request(self, *args, **kwargs):
        retries = 0

        while True:
            response = super().request(*args, **kwargs)

            try:
                check_response_valid(response)
            except RateLimitError as e:
                retries += 1
                if retries > self.max_retries:
                    raise RuntimeError(f"Rate limit retry exceeded ({self.max_retries} attempts).") from e

                retry_after = response.headers.get("Retry-After")
                try:
                    wait_time = int(retry_after)
                except (TypeError, ValueError):
                    wait_time = 2

                print(f"Rate limited. Sleeping {wait_time} seconds before retrying... (attempt {retries})")
                time.sleep(wait_time)
                continue

            return response