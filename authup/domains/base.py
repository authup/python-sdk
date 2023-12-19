from typing import Any

from authup.domains.clients.client import AuthupClient
from authup.domains.types_base import BaseAPIContext


class BaseAPI:
    client: AuthupClient

    def __int__(self, context: BaseAPIContext = None):
        self.set_client(context.client)

    def set_client(self, input: Any):
        if isinstance(input, AuthupClient):
            self.client = input
        else:
            self.client = AuthupClient(input.authup_url,
                                       input.username,
                                       input.password,
                                       input.robot_id,
                                       input.robot_secret,
                                       )
