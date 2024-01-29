from enum import Enum
from typing import Optional

from pydantic import BaseModel

from ..client.types import Client
from ..realm.types import Realm
from ..user.types import User


class OAuth2AuthorizationResponseType(Enum):
    NONE = "none"
    CODE = "code"
    TOKEN = "token"
    ID_TOKEN = "id_token"


class OAuth2AuthorizationCode(BaseModel):
    id: str
    content: str
    expires: str
    scope: Optional[str]
    redirect_uri: Optional[str]
    id_token: Optional[str]
    client_id: Optional[str]
    client: Optional[Client]
    user_id: Optional[str]
    user: Optional[User]
    realm_id: str
    realm: Realm


class OAuth2AuthorizationCodeRequest(BaseModel):
    response_type: Optional[OAuth2AuthorizationResponseType]
    client_id: Optional[str]
    redirect_uri: Optional[str]
    scope: Optional[str]
    state: Optional[str]
