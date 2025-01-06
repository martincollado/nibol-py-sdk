from typing import List, Any
from nibol.models.user import UserListRequest, UserResponse


class UserApi:
    def __init__(self, client: Any):
        self.client = client

    async def list_users(self, payload: UserListRequest) -> List[UserResponse]:
        """Retrieve users by IDs or emails."""
        response = await self.client.request(
            method="POST",
            endpoint="/v1/user/list",
            json=payload.dict(exclude_none=True),
        )
        return [UserResponse(**user) for user in response]
