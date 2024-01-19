from datetime import datetime
from typing import Optional

from ...constants import DomainType
from ...permission.types import PermissionRelation
from ...realm.types import Realm
from ...types_base import DomainEventBaseContext
from ..types import User


class UserPermission(PermissionRelation):
    id: str
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    user_id: str
    user: Optional[User]
    user_realm_id: Optional[str]
    user_realm: Optional[Realm]


class UserPermissionEventContext(DomainEventBaseContext):
    type: str = DomainType.USER_PERMISSION.value
    data: UserPermission


class UserPermissionCreate(UserPermission):
    id: Optional[str]
    pass
