from ..base_api_client import ResourceClient
from ..robot.types import Robot, RobotCreate, RobotUpdate


class RobotClient(ResourceClient[Robot, RobotCreate, RobotUpdate]):
    async def integrity(self, id: str) -> str:
        response = await self.client.get(f"robots/{id}/integrity")
        response.raise_for_status()
        return id

    pass