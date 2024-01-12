from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..constants import DomainType

# from ..permission.types import Permission
from ..realm.types import Realm
from ..types_base import DomainEventBaseContext


class User(BaseModel):
    id: str
    name: str
    name_locked: bool = False
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
    active: bool = False
    active_hash: Optional[str] = None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    realm_id: str
    realm: Optional[Realm]

    # TODO: token, permission?
    # token: Optional[str] = None
    # permissions: Optional[List[Permission]] = None


class UserEventContext(DomainEventBaseContext):
    type: str = f"{DomainType.USER}"
    data: User


class UserCreate(User):
    id: Optional[str]
    realm_id: Optional[str]
    pass


class UserUpdate(User):
    id: Optional[str]
    realm_id: Optional[str]
    updated_at: str = datetime.now().isoformat()
    pass


# class UserResponse(BaseModel): # TODO
#     user: User
#     token: dict
