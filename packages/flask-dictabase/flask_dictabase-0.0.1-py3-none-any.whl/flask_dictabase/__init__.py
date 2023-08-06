import dataset
from flask import current_app, _app_ctx_stack


class Dictabase:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('DICTABASE_URL', 'sqlite:///dictabase.db')
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'dictabase'):
            ctx.dictabase.close()

    @property
    def db(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'dictabase'):
                ctx.dictabase = dataset.connect(self.app.config['DICTABASE_URL'])
        return ctx.dictabase

    def FindAll(self, cls, **kwargs):
        tableName = cls.__name__
        return self.db[tableName].all(**kwargs)

    def New(self, cls, **kwargs):
        self.db.begin()
        tableName = cls.__name__
        obj = cls(**kwargs)
        self.db[tableName].insert(obj)
        self.db.commit()

    def Upsert(self, obj):
        tableName = type(obj).__name__
        self.db.begin()
        self.db[tableName].upsert(dict(obj), ['id'])  # find row with matching 'id' and update it
        self.db.commit()
