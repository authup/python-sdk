from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..constants import DomainType
from ..types_base import DomainEventBaseContext
from .realm import Realm


class Role(BaseModel):
    id: Optional[str]
    name: str
    target: Optional[str] = None
    description: Optional[str] = None
    realm_id: Optional[str] = None
    realm: Optional[Realm] = None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class RoleEventContext(DomainEventBaseContext):
    type: str = f"{DomainType.ROLE}"
    data: Role


class RoleCreate(Realm):
    pass


class RoleUpdate(Realm):
    updated_at: str = datetime.now().isoformat()
    pass
