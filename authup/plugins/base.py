from authup import Authup


class AuthupPluginBase:
    def __init__(
        self,
        url: str = None,
        username: str = None,
        password: str = None,
        robot_id: str = None,
        robot_secret: str = None,
    ):
        self.authup = Authup(
            url=url,
            username=username,
            password=password,
            robot_id=robot_id,
            robot_secret=robot_secret,
        )
