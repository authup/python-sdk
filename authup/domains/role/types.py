from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..constants import DomainType
from ..realm.types import Realm
from ..types_base import DomainEventBaseContext


class Role(BaseModel):
    id: str
    name: str
    target: Optional[str] = None
    description: Optional[str] = None
    realm_id: Optional[str]
    realm: Optional[Realm] = None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class RoleEventContext(DomainEventBaseContext):
    type: str = f"{DomainType.ROLE}"
    data: Role


class RoleCreate(Role):
    id: Optional[str]
    pass


class RoleUpdate(Role):
    id: Optional[str]
    updated_at: str = datetime.now().isoformat()
    pass
