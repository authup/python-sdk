from datetime import datetime
from typing import Optional

from ...constants import DomainType
from ...permission.types import PermissionRelation
from ...realm.types import Realm
from ...robot.types import Robot
from ...types_base import DomainEventBaseContext


class RobotPermission(PermissionRelation):
    id: str
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    robot_id: str
    robot: Robot
    robot_realm_id: Optional[str]
    robot_realm: Optional[Realm]


class RobotPermissionEventContext(DomainEventBaseContext):
    type: str = DomainType.ROBOT_PERMISSION
    data: RobotPermission


class RobotPermissionCreate(RobotPermission):
    id: Optional[str]
    pass
