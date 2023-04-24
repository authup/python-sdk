from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RealmBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    drop_able: Optional[bool] = None


class RealmCreate(RealmBase):
    pass


class RealmUpdate(RealmBase):
    pass


class Realm(RealmBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
