import datetime
from typing import List, Optional

from pydantic import BaseModel


class Permission(BaseModel):
    inverse: Optional[bool] = False
    name: str
    power: int
    condition: Optional[str] = None
    target: Optional[str] = None


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
    permissions: Optional[List[Permission]] = None
    status: Optional[str] = None
    status_message: Optional[str] = None


class TokenIntrospectionResponse(BaseModel):
    active: bool
    client_id: str | None
    exp: int
    iat: int
    iss: str
    jti: str
    scope: str
    sub: str
    kind: str
    realm_id: str
    realm_name: str
    username: str | None
    preferred_username: str
    family_name: str | None
    given_name: str | None
    name: str
    nickname: str
    email: str
    email_verified: bool
    updated_at: int
    permissions: Optional[List[Permission]] = None


class TokenResponse(BaseModel):
    token_type: str
    expires_in: int
    access_token: str
    refresh_token: Optional[str] = None


class UserResponse(BaseModel):
    user: User
    token: dict
