import dictabase
from flask import current_app, _app_ctx_stack

global worker
dictabase.RegisterDBURI()


class Dictabase:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        pass

    def teardown(self, exception):
        pass

    def FindAll(self, *args, **kwargs):
        return dictabase.FindAll(*args, **kwargs)

    def FindOne(self, *args, **kwargs):
        return dictabase.FindOne(*args, **kwargs)

    def New(self, *args, **kwargs):
        return dictabase.New(*args, **kwargs)

    def Delete(self, *args, **kwargs):
        return dictabase.Delete(*args, **kwargs)

    def Drop(self, *args, **kwargs):
        return dictabase.Drop(*args, **kwargs)


class BaseTable(dictabase.BaseTable):
    pass
