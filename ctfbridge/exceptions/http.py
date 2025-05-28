from .base import CTFBridgeError


class APIError(CTFBridgeError):
    def __init__(self, message: str, *, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class BadRequestError(APIError):
    pass


class UnauthorizedError(APIError):
    pass


class ForbiddenError(APIError):
    pass


class NotFoundError(APIError):
    pass


class ConflictError(APIError):
    pass


class ValidationError(APIError):
    pass


class ServerError(APIError):
    pass


class ServiceUnavailableError(APIError):
    pass


class RateLimitError(APIError):
    def __init__(self, retry_after: int | None = None):
        msg = "Rate limit exceeded."
        if retry_after:
            msg += f" Retry after {retry_after} seconds."
        super().__init__(msg)
        self.retry_after = retry_after
