from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ...constants import DomainType
from ...realm.types import Realm
from ...role.types import Role
from ...types_base import DomainEventBaseContext
from ..types import User


class UserRole(BaseModel):
    id: str
    role_id: str
    role: Role
    role_realm_id: Optional[str]
    role_realm: Optional[Realm]
    user_id: str
    user: User
    user_realm_id: Optional[str]
    user_realm: Optional[Realm]
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class UserRoleEventContext(DomainEventBaseContext):
    type: str = DomainType.USER_ROLE
    data: UserRole


class UserRoleCreate(UserRole):
    id: Optional[str]
    pass


class UserRoleUpdate(UserRole):
    raise Exception("No Update function available for UserRole object.")
