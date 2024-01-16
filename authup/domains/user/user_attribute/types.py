from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ...constants import DomainType
from ...realm.types import Realm
from ...types_base import DomainEventBaseContext
from ..types import User


class UserAttribute(BaseModel):
    id: str
    name: str
    value: Optional[str]
    user_id: str
    user: User
    realm_id: str
    realm: Realm
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class UserAttributeEventContext(DomainEventBaseContext):
    type: str = DomainType.USER_ATTRIBUTE
    data: UserAttribute


class UserAttributeCreate(UserAttribute):
    id: Optional[str]
    pass


class UserAttributeUpdate(UserAttribute):
    id: Optional[str]
    updated_at = datetime.now().isoformat()
    pass
