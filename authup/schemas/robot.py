from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from authup.schemas.realm import Realm
from authup.schemas.user import User


class RobotBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    secret: Optional[str] = None
    active: Optional[bool] = None
    realm_id: Optional[str] = None
    user_id: Optional[str] = None


class RobotCreate(RobotBase):
    pass


class RobotUpdate(RobotBase):
    pass


class Robot(RobotBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[User] = None
    realm: Optional[Realm] = None
