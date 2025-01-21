from typing import Any, List, Optional, Union, Coroutine
from pydantic import ValidationError
from nibol.models.user import UserListRequest, User


class UserAPI:
    """
    Manages user listing (sync or async) with a unified request approach.
    """

    def __init__(self, client: Any):
        # Detect if the client is async by checking for 'arequest' or class name.
        self.client = client
        self.is_async = hasattr(client, "arequest") or client.__class__.__name__.startswith("Async")
        self.log = getattr(client, "logger", None)

    def _log(self, message: str, **kwargs) -> None:
        if self.log:
            self.log.info(message, **kwargs)

    async def _execute_request_async(self, method: str, endpoint: str, payload: Optional[dict] = None) -> Any:
        """
        Internal method to execute an async request using the client's async method.
        """
        try:
            return await self.client.request(method=method, endpoint=endpoint, json=payload)
        except Exception as e:
            if self.log:
                self.log.error("unexpected_error", mode="async", endpoint=endpoint, error=str(e))
            raise

    def _execute_request_sync(self, method: str, endpoint: str, payload: Optional[dict] = None) -> Any:
        """
        Internal method to execute a sync request using the client's sync method.
        """
        try:
            return self.client.request(method=method, endpoint=endpoint, json=payload)
        except Exception as e:
            if self.log:
                self.log.error("unexpected_error", mode="sync", endpoint=endpoint, error=str(e))
            raise

    def _request(
        self, method: str, endpoint: str, payload: Optional[dict] = None
    ) -> Union[Any, Coroutine[Any, Any, Any]]:
        """
        Dispatch method that calls the appropriate sync or async request method.
        Returns the raw response or a coroutine, depending on `is_async`.
        """
        if self.is_async:
            return self._execute_request_async(method, endpoint, payload)
        return self._execute_request_sync(method, endpoint, payload)

    def list_users(
        self, emails: Optional[List[str]] = None, ids: Optional[List[str]] = None
    ) -> Union[List[User], Coroutine[Any, Any, List[User]]]:
        """
        Retrieve a list of users filtered by emails or ids.
        Returns a list if sync, or a coroutine if async.
        """
        self._log("listing_users", mode="auto", emails=emails, ids=ids)

        try:
            req_data = UserListRequest(emails=emails, ids=ids)
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", error=str(e))
            raise

        response = self._request("POST", "/v1/user/list", payload=req_data.model_dump(exclude_none=True))

        if self.is_async:

            async def async_result():
                try:
                    raw = await response
                    users = [User(**user) for user in raw]
                    self._log("users_listed", mode="async", count=len(users))
                    return users
                except ValidationError as e:
                    if self.log:
                        self.log.error("validation_error", mode="async", error=str(e))
                    raise

            return async_result()

        try:
            users = [User(**user) for user in response]
            self._log("users_listed", mode="sync", count=len(users))
            return users
        except ValidationError as e:
            if self.log:
                self.log.error("validation_error", mode="sync", error=str(e))
            raise
