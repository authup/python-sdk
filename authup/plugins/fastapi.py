from typing import List, Union

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from authup.permissions import check_permissions
from authup.schemas import Permission, User
from authup.token import get_user_from_token_async, introspect_token_async


class AuthupUser:
    def __init__(self, url: str):
        self.url = url
        self.user_url = url + "/users" + "/@me"

    async def __call__(
        self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> User:
        try:
            user = await get_user_from_token_async(
                self.user_url, credentials.credentials
            )

        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
        return user


class UserPermissions(AuthupUser):
    def __init__(
        self,
        url: str,
        permissions: Union[List[Permission], List[str], List[dict]] = None,
    ):
        super().__init__(url)
        self.permissions = permissions

    async def __call__(
        self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> User:
        # Get the user
        user = await super().__call__(credentials)
        permission = await introspect_token_async(
            token_introspect_url=self.url + "/token/introspect",
            token=credentials.credentials,
        )
        user.permissions = permission.permissions
        # Check the permissions
        authorized = check_permissions(user.permissions, self.permissions)

        if not authorized:
            raise HTTPException(status_code=401, detail="Insufficient permissions")
        return user
