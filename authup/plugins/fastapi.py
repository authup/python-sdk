from typing import List, Union

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from authup.permissions import check_permissions
from authup.schemas.token import Permission
from authup.schemas.user import User
from authup.token import get_user_from_token_async, introspect_token_async


class AuthupUser:
    def __init__(
        self,
        url: str,
        permissions: Union[List[Permission], List[str], List[dict]] = None,
    ):
        self.url = url
        self.user_url = url + "/users" + "/@me"
        self.introspect_url = url + "/token/introspect"
        self.permissions = permissions

    async def __call__(
        self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> User:
        try:
            # get the user from the token
            user = await get_user_from_token_async(
                self.user_url, credentials.credentials
            )
            # if permissions are set, check them
            if self.permissions:
                permissions = await introspect_token_async(
                    token_introspect_url=self.introspect_url,
                    token=credentials.credentials,
                )
                # add the permissions to the user
                user.permissions = permissions.permissions
                check_permissions(user.permissions, self.permissions)
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
        yield user
