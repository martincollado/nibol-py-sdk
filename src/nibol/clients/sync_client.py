import httpx
from typing import Optional, Dict, Any
from nibol.exceptions import (
    ValidationError,
    AuthenticationError,
    PermissionError,
    NotFoundError,
    RateLimitExceededError,
    ServerError,
    ApiError,
)


class SyncApiClient:
    """
    Synchronous HTTP client to interact with an API,
    handling custom exceptions for specific HTTP status codes.
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        user_email: Optional[str] = None,
        timeout: int = 10,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.user_email = user_email
        self.timeout = timeout
        self.headers = self._build_headers()
        self.client = httpx.Client(timeout=self.timeout)

    def _build_headers(self) -> Dict[str, str]:
        headers = {}
        if self.api_key:
            headers["api_key"] = self.api_key
        if self.user_email:
            headers["user_email"] = self.user_email
        return headers

    def _handle_errors(self, response: httpx.Response) -> None:
        """
        Maps specific HTTP status codes to custom exceptions.
        Raises them if the status code indicates an error.
        """
        error_map = {
            400: ValidationError,
            401: AuthenticationError,
            403: PermissionError,
            404: NotFoundError,
            429: RateLimitExceededError,
        }

        if response.status_code in error_map:
            raise error_map[response.status_code](f"{error_map[response.status_code].__name__}: {response.text}")
        elif 400 <= response.status_code < 500:
            # Client errors not explicitly mapped
            raise ApiError(f"ApiError: {response.status_code} - {response.text}")
        elif response.status_code >= 500:
            # Server errors
            raise ServerError(f"ServerError: {response.text}")

    def request(
        self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Perform an HTTP request with the given method, endpoint, and optional params/json.
        Raises custom exceptions based on the response status code.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.client.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=json,
        )
        self._handle_errors(response)
        return response.json()
