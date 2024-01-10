from datetime import datetime
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
