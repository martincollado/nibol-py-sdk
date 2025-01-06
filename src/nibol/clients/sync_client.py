import requests
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
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        user_email: Optional[str] = None,
        timeout: int = 10,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.user_email = user_email
        self.timeout = timeout
        self.headers = self._build_headers()

    def _build_headers(self) -> Dict[str, str]:
        headers = {}
        if self.api_key:
            headers["api_key"] = self.api_key
        if self.user_email:
            headers["user_email"] = self.user_email
        return headers

    def _handle_errors(self, response: requests.Response):
        if response.status_code == 400:
            raise ValidationError(f"ValidationError: {response.text}")
        elif response.status_code == 401:
            raise AuthenticationError(f"AuthenticationError: {response.text}")
        elif response.status_code == 403:
            raise PermissionError(f"PermissionError: {response.text}")
        elif response.status_code == 404:
            raise NotFoundError(f"NotFoundError: {response.text}")
        elif response.status_code == 429:
            raise RateLimitExceededError(f"RateLimitExceededError: {response.text}")
        elif response.status_code >= 500:
            raise ServerError(f"ServerError: {response.text}")
        elif response.status_code >= 400:
            raise ApiError(f"ApiError: {response.status_code} - {response.text}")

    def request(
        self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None
    ) -> Any:
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        response = requests.request(method, url, headers=self.headers, params=params, json=json, timeout=self.timeout)
        self._handle_errors(response)
        return response.json()
