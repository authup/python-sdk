from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel

R = TypeVar("R")


class SingleResourceResponse(Generic[R]):
    data: R


class CollectionResourceResponse(Generic[R]):
    data: List[R]
    meta: Dict[str, int]


class DomainEntityWithID(BaseModel):
    id: Any


T = TypeVar("T", bound=DomainEntityWithID)


class DomainAPISlim(Generic[T]):
    def get_many(self, record: Any = None) -> CollectionResourceResponse[T]:
        pass

    def get_one(self, id: Any, record: Any = None) -> SingleResourceResponse[T]:
        pass

    def delete(self, id: Any) -> SingleResourceResponse[T]:
        pass

    def create(self, data: Any) -> SingleResourceResponse[T]:
        pass


class DomainAPI(DomainAPISlim[T]):
    def update(self, id: Any, data: Any) -> SingleResourceResponse[T]:
        pass


class BaseAPIContext(BaseModel):
    client: Optional[Any]


class DomainEventBaseContext(BaseModel):
    event: str  # DomainEventName
    type: str
