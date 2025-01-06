from pydantic import BaseModel, constr
from typing import List, Optional, Annotated


class UserListRequest(BaseModel):
    ids: Optional[List[Annotated[str, constr(regex="^[a-f\\d]{24}$")]]]
    emails: Optional[List[str]]


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    picture: Optional[str]
    status: Optional[str]
