class AuthupFlask:
    def __init__(self, app=None, authup_url=None):
        if app is not None:
            self.init_app(app, authup_url)

    def init_app(self, app):
        app.before_request(self.before_request)

    def before_request(self):
        pass
