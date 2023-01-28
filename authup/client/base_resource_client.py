from typing import Generic, List, Type, TypeVar

from httpx import AsyncClient
from pydantic import BaseModel

ResourceType = TypeVar("ResourceType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ResourceClient(Generic[ResourceType, CreateSchemaType, UpdateSchemaType]):
    """Base class for resource clients."""

    def __init__(
        self, model: Type[ResourceType], client: AsyncClient, prefix: str = None
    ):
        self.model = model
        self.client = client
        if prefix:
            if not prefix.startswith("/"):
                prefix = "/" + prefix
        self.prefix = prefix

    def _format_url(self, resource_id: str = None):
        if resource_id:
            url = f"{self.prefix}/{resource_id}"
            return url
        return self.prefix

    async def get(self, id: str) -> ResourceType:
        url = self._format_url(id)
        response = await self.client.get(url)
        response.raise_for_status()
        return self.model.parse_raw(response.text)

    async def get_many(self) -> List[ResourceType]:
        url = self._format_url()
        response = await self.client.get(url)
        response.raise_for_status()
        return [self.model(**item) for item in response.json()["data"]]

    async def create(self, data: CreateSchemaType) -> ResourceType:
        url = self._format_url()
        response = await self.client.post(url, json=data.dict())
        response.raise_for_status()
        return self.model.parse_raw(response.content)

    async def update(self, id: str, data: UpdateSchemaType) -> ResourceType:
        url = self._format_url(id)
        response = await self.client.post(url, json=data.dict())
        response.raise_for_status()
        return self.model(**response.json())

    async def delete(self, id: str) -> str:
        url = self._format_url(id)
        response = await self.client.delete(url)
        response.raise_for_status()
        return id
