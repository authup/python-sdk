from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from authup.domains.constants import DomainType
from authup.domains.schemas.realm import Realm
from authup.domains.types_base import DomainEventBaseContext


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
