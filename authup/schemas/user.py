import datetime
from typing import List, Optional

from pydantic import BaseModel

from authup.schemas.token import Permission


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


class UserResponse(BaseModel):
    user: User
    token: dict
