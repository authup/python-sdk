from datetime import datetime
from typing import Optional, TypeVar

from pydantic import BaseModel

from authup.domains.schemas.realm import Realm
from authup.domains.types_base import DomainEventBaseContext
from authup.domains.constants import DomainType


class Permission(BaseModel):
    id: str
    built_in: bool
    name: str
    description: Optional[str] = None
    target: Optional[str] = None
    realm_id: Optional[Realm.id] = None
    realm: Optional[Realm] = None
    created_at: datetime
    updated_at: datetime


class PermissionEventContext(DomainEventBaseContext):
    type: str  # f'{DomainType.PERMISSION}'
    data: Permission


class PermissionRelation(BaseModel):
    power: int
    condition: Optional[str] = None
    fields: Optional[str] = None
    negation: bool
    target: Optional[str] = None
    permission_id: Permission.id
    permission: Permission
    permission_realm_id: Optional[Realm.id] = None
    permission_realm: Optional[Realm] = None


class PermissionCreate(Permission):
    pass


class PermissionUpdate(Permission):
    pass
