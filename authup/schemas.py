import datetime
from typing import List, Optional

from pydantic import BaseModel


def to_camel(string: str) -> str:
    split = string.split("_")
    return split[0] + "".join(word.capitalize() for word in split[1:])


class UserPermission(BaseModel):
    id: str
    negation: bool
    power: int
    condition: Optional[str] = None
    fields: Optional[List[str]] = None


class User(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    active: bool
    token: Optional[str] = None
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    realm_id: str
    display_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name_locked: bool
    permissions: Optional[List[UserPermission]] = None
    status: Optional[str] = None
    status_message: Optional[str] = None


class Token(BaseModel):
    exp: int
    iat: int
    iss: str
    remote_address: str
    sub: str
    sub_kind: str

    class Config:
        alias_generator = to_camel


class UserResponse(BaseModel):
    user: User
    token: dict
