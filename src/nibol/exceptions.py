class ApiError(Exception):
    def __init__(self, status_code: int, detail: str = None):
        self.status_code = status_code
        self.detail = detail or "An unknown error occurred."
        super().__init__(f"API Error {status_code}: {self.detail}")


class ValidationError(ApiError):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=400, detail=detail)


class AuthenticationError(ApiError):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=401, detail=detail)


class PermissionError(ApiError):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(status_code=403, detail=detail)


class NotFoundError(ApiError):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class ServerError(ApiError):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=500, detail=detail)


class RateLimitExceededError(ApiError):
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(status_code=429, detail=detail)
