from typing import List, Optional

from pydantic import BaseModel


class Permission(BaseModel):
    inverse: Optional[bool] = False
    name: str
    power: int
    condition: Optional[str] = None
    target: Optional[str] = None


class TokenIntrospectionResponse(BaseModel):
    active: bool
    client_id: Optional[str] = None
    exp: int
    iat: int
    iss: str
    jti: str
    scope: str
    sub: str
    kind: str
    realm_id: str
    realm_name: str
    username: Optional[str] = None
    preferred_username: str
    family_name: Optional[str] = None
    given_name: Optional[str] = None
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
