from pydantic import BaseModel, constr
from typing import List, Optional, Annotated


class UserListRequest(BaseModel):
    ids: Optional[List[Annotated[str, constr(pattern="^[a-f\\d]{24}$")]]] = None
    emails: Optional[List[str]] = None


class UserResponse(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    active: Optional[bool]
