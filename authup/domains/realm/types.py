from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..constants import DomainType
from ..types_base import DomainEventBaseContext


class Realm(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    built_in: bool = False
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class RealmEventContext(DomainEventBaseContext):
    type: str = f"{DomainType.REALM}"
    data: Realm


class RealmCreate(Realm):
    id: Optional[str]
    pass


class RealmUpdate(Realm):
    id: Optional[str]
    updated_at = datetime.now().isoformat()
    pass


REALM_MASTER_NAME = "master"
