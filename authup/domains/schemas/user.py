from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

# from authup.domains.schemas.permission import Permission
from authup.domains.schemas.realm import Realm
from authup.domains.types_base import DomainEventBaseContext
from authup.domains.constants import DomainType


class User(BaseModel):
    id: str
    name: str
    name_locked: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: str
    email: Optional[str] = None
    password: Optional[str] = None
    avatar: Optional[str] = None
    cover: Optional[str] = None
    reset_hash: Optional[str] = None
    reset_at: Optional[str] = None
    reset_expires: Optional[str] = None
    status: Optional[str] = None
    status_message: Optional[str] = None
    active: bool
    active_hash: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    realm_id: str
    realm: Realm

    # TODO: token, permission?
    # token: Optional[str] = None
    # permissions: Optional[List[Permission]] = None


class UserEventContext(DomainEventBaseContext):
    type: str  # f'{DomainType.USER}'
    data: User


class UserCreate(User):
    pass


class UserUpdate(User):
    pass


# class UserResponse(BaseModel): # TODO
#     user: User
#     token: dict
