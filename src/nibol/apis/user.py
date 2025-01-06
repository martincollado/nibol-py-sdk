from typing import List, Any
from pydantic import ValidationError
from nibol.models.user import UserListRequest, User


class UserApi:
    def __init__(self, client: Any):
        self.client = client

    def list_users(self, emails: list[str] = None, ids: list[str] = None) -> List[dict]:
        try:
            request_data = UserListRequest(emails=emails, ids=ids)

            response = self.client.request(
                method="POST",
                endpoint="/v1/user/list",
                json=request_data.model_dump(exclude_none=True),
            )

            return [User(**user) for user in response]
        except ValidationError as e:
            print(e)
