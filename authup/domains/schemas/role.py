from datetime import datetime
from typing import Optional, TypeVar

from pydantic import BaseModel

from authup.domains.schemas.realm import Realm
from authup.domains.constants import DomainType
from authup.domains.base import DomainEventBaseContext


class Role(BaseModel):
    id: str
    name: str
    target: Optional[str] = None
    description: Optional[str] = None
    realm_id: Optional[Realm.id] = None
    realm: Optional[Realm] = None
    created_at: datetime
    updated_at: datetime


class RoleEventContext(DomainEventBaseContext):
    type: str  # f'{DomainType.ROLE}'
    data: Role


class RoleCreate(Realm):
    pass


class RoleUpdate(Realm):
    pass
