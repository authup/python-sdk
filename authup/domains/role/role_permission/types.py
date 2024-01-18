from datetime import datetime
from typing import Optional

from ...constants import DomainType
from ...permission.types import PermissionRelation
from ...realm.types import Realm
from ...role.types import Role
from ...types_base import DomainEventBaseContext


class RolePermission(PermissionRelation):
    id: str
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    role_id: str
    role: Role
    role_realm_id: Optional[str]
    role_realm: Optional[Realm]


class RolePermissionEventContext(DomainEventBaseContext):
    type: str = DomainType.ROLE_PERMISSION
    data: RolePermission


class RolePermissionCreate(RolePermission):
    id: Optional[str]
    pass
