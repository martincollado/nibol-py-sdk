import httpx
from typing import Optional, Dict, Any
from nibol.exceptions import (
    ApiError,
    ValidationError,
    AuthenticationError,
    PermissionError,
    NotFoundError,
    ServerError,
    RateLimitExceededError,
)


class AsyncApiClient:
    def __init__(
        self, base_url: str, api_key: Optional[str] = None, user_email: Optional[str] = None, timeout: int = 10
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.user_email = user_email
        self.timeout = timeout
        self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)
        self.headers = self._build_headers()

    def _build_headers(self) -> Dict[str, str]:
        headers = {}
        if self.api_key:
            headers["api_key"] = self.api_key
        if self.user_email:
            headers["user_email"] = self.user_email
        return headers

    def _handle_errors(self, response: httpx.Response):
        if response.status_code == 400:
            raise ValidationError(response.text)
        elif response.status_code == 401:
            raise AuthenticationError(response.text)
        elif response.status_code == 403:
            raise PermissionError(response.text)
        elif response.status_code == 404:
            raise NotFoundError(response.text)
        elif response.status_code == 429:
            raise RateLimitExceededError(response.text)
        elif response.status_code >= 500:
            raise ServerError(response.text)
        elif response.status_code >= 400:
            raise ApiError(response.status_code, response.text)

    async def request(
        self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None
    ) -> Any:
        response = await self.client.request(method, endpoint, headers=self.headers, params=params, json=json)
        self._handle_errors(response)
        return response.json()

    async def close(self):
        if self.client:
            await self.client.aclose()
