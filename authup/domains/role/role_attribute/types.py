from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ...constants import DomainType
from ...realm.types import Realm
from ...role.types import Role
from ...types_base import DomainEventBaseContext


class RoleAttribute(BaseModel):
    id: str
    name: str
    value: Optional[str]
    role_id = str
    role: Optional[Role]
    realm_id: Optional[str]
    role_realm: Optional[Realm]
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class RoleAttributeEventContext(DomainEventBaseContext):
    type: str = DomainType.ROLE_ATTRIBUTE.value
    data: RoleAttribute


class RoleAttributeCreate(RoleAttribute):
    id: Optional[str]
    pass


class RoleAttributeUpdate(RoleAttribute):
    id: Optional[str]
    updated_at: str = datetime.now().isoformat()
    pass
