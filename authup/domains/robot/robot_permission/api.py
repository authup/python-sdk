from ...base_api_client import ResourceClient
from .types import RobotPermission, RobotPermissionCreate, RobotPermissionUpdate


class RobotPermissionAPI(
    ResourceClient[RobotPermission, RobotPermissionCreate, RobotPermissionUpdate]
):
    pass
