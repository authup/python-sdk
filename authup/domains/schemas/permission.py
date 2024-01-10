from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from ..constants import DomainType
from ..types_base import DomainEventBaseContext
from .realm import Realm


class Permission(BaseModel):
    id: Optional[str]
    built_in: bool = False
    name: str
    description: Optional[str] = None
    target: Optional[str] = None
    realm_id: Optional[str] = None
    realm: Optional[Realm] = None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class PermissionEventContext(DomainEventBaseContext):
    type: str = f"{DomainType.PERMISSION}"
    data: Permission


class PermissionRelation(BaseModel):
    power: int
    condition: Optional[str] = None
    fields: Optional[str] = None
    negation: bool
    target: Optional[str] = None
    permission_id: str
    permission: Permission
    permission_realm_id: Optional[str] = None
    permission_realm: Optional[Realm] = None


class PermissionCreate(Permission):
    pass


class PermissionUpdate(Permission):
    updated_at: str = datetime.now().isoformat()
    pass


class PermissionName(Enum):
    CLIENT_ADD = "client_add"
    CLIENT_DROP = "client_drop"
    CLIENT_EDIT = "client_edit"

    PROVIDER_ADD = "provider_add"
    PROVIDER_DROP = "provider_drop"
    PROVIDER_EDIT = "provider_edit"

    PERMISSION_ADD = "permission_add"
    PERMISSION_DROP = "permission_drop"
    PERMISSION_EDIT = "permission_edit"

    REALM_ADD = "realm_add"
    REALM_DROP = "realm_drop"
    REALM_EDIT = "realm_edit"

    ROBOT_ADD = "robot_add"
    ROBOT_DROP = "robot_drop"
    ROBOT_EDIT = "robot_edit"

    ROBOT_PERMISSION_ADD = "robot_permission_add"
    ROBOT_PERMISSION_DROP = "robot_permission_drop"

    ROBOT_ROLE_ADD = "robot_role_add"
    ROBOT_ROLE_DROP = "robot_role_drop"
    ROBOT_ROLE_EDIT = "robot_role_edit"

    ROLE_ADD = "role_add"
    ROLE_DROP = "role_drop"
    ROLE_EDIT = "role_edit"

    ROLE_PERMISSION_ADD = "role_permission_add"
    ROLE_PERMISSION_DROP = "role_permission_drop"

    SCOPE_ADD = "scope_add"
    SCOPE_DROP = "scope_drop"
    SCOPE_EDIT = "scope_edit"

    TOKEN_VERIFY = "token_verify"

    USER_ADD = "user_add"
    USER_DROP = "user_drop"
    USER_EDIT = "user_edit"

    USER_PERMISSION_ADD = "user_permission_add"
    USER_PERMISSION_DROP = "user_permission_drop"

    USER_ROLE_ADD = "user_role_add"
    USER_ROLE_DROP = "user_role_drop"
    USER_ROLE_EDIT = "user_role_edit"
