from typing import List, Any
from nibol.models.user import UserListRequest, UserResponse


class UserApi:
    def __init__(self, client: Any):
        self.client = client

    def list_users(self, emails: list[str] = None, ids: list[str] = None) -> List[dict]:
        """Retrieve users by IDs or emails.

        Args:
            emails: Optional list of email addresses
            ids: Optional list of user IDs

        Returns:
            List of user dictionaries

        Raises:
            ValueError: If neither emails nor ids are provided
        """
        if not emails and not ids:
            raise ValueError("At least one of emails or ids must be provided")

        request_data = UserListRequest(emails=emails, ids=ids)

        response = self.client.request(
            method="POST",
            endpoint="/v1/user/list",
            json=request_data.model_dump(exclude_none=True),
        )

        validated_users = [UserResponse(**user) for user in response]
        return [user.model_dump() for user in validated_users]
