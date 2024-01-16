from typing import Optional

from pydantic import BaseModel

from ...client.types import Client
from ...constants import DomainType
from ...scope.types import Scope
from ...types_base import DomainEventBaseContext


class ClientScope(BaseModel):
    id: str
    default: bool = False
    client_id = str
    client: Client
    scope_id = str
    scope = Scope


class ClientScopeEventContext(DomainEventBaseContext):
    type: str = f"{DomainType.CLIENT_SCOPE}"
    data: ClientScope


class ClientScopeCreate(ClientScope):
    id: Optional[str]
    pass


class ClientScopeUpdate(ClientScope):
    raise Exception("No Update function available for ClientScope object.")
