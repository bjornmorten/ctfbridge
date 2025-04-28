from ..exceptions import RateLimitError, SessionExpiredError


def check_response_valid(response):
    """
    Checks if the HTTP response indicates a session expiration or rate limiting.
    Raises appropriate exceptions if problems are detected.
    """
    if response.status_code == 401 or response.status_code == 403:
        raise SessionExpiredError("Session expired or unauthorized. Please login again.")
    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After", "unknown")
        raise RateLimitError(f"Rate limited. Retry after {retry_after} seconds.")
