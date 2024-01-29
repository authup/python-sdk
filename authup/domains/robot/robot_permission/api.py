from pydantic import BaseModel

from ...base_api_client import ResourceClient
from .types import RobotPermission, RobotPermissionCreate


class RobotPermissionAPI(
    ResourceClient[RobotPermission, RobotPermissionCreate, BaseModel]
):
    pass
