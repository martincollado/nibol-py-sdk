from pydantic import BaseModel, constr, model_validator
from typing import List, Optional, Annotated

from pydantic_core import PydanticCustomError


class UserListRequest(BaseModel):
    ids: Optional[List[Annotated[str, constr(pattern="^[a-f\\d]{24}$")]]] = None
    emails: Optional[List[str]] = None

    @model_validator(mode="after")
    def check_ids_or_emails(cls, values):
        if not values.ids and not values.emails:
            # Personalización del error
            raise PydanticCustomError(
                "missing_filter", "You must provide at least one of 'ids' or 'emails' to filter the users."
            )
        return values


class User(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    active: Optional[bool]
