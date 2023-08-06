import dictabase
import dataset
from flask import _app_ctx_stack, current_app


class Dictabase:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('DATABASE_URL', 'sqlite:///dictabase.db')
        app.teardown_appcontext(self.teardown)

    @property
    def db(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'db'):
                ctx.db = dataset.connect(current_app.config['DATABASE_URL'])
        return ctx.db

    def teardown(self, exception):
        self.db.close()

    def FindAll(self, cls, **kwargs):
        for obj in self.db[cls.__name__].find(**kwargs):
            yield cls(db=self.db, **obj)

    def FindOne(self, cls, **kwargs):
        ret = self.db[cls.__name__].find_one(**kwargs)
        ret = cls(db=self.db, **ret)
        return ret

    def New(self, cls, **kwargs):
        self.db.begin()
        newID = self.db[cls.__name__].insert(dict(**kwargs))
        print('insert return=', newID)
        self.db.commit()
        ret = cls(db=self.db, id=newID, **kwargs)
        return ret

    def Upsert(self, obj):
        self.db.begin()
        ret = self.db[type(obj).__name__].upsert(dict(obj), ['id'])
        self.db.commit()
        return ret

    def Delete(self, obj):
        print('Delete(obj=', obj)
        self.db.begin()
        ret = self.db[type(obj).__name__].delete(id=obj['id'])
        self.db.commit()
        return ret

    def Drop(self, cls, confirm=False):
        if confirm is False:
            raise Exception('You must pass confirm=True to Drop a table.')
        self.db.begin()
        ret = self.db[cls.__name__].drop()
        self.db.commit()
        return ret


class BaseTable(dict):
    def __init__(self, *a, **k):
        self.db = k.pop('db')
        super().__init__(*a, **k)

    def Commit(self):
        print('Commit(self=', self)
        self.db.begin()
        ret = self.db[type(self).__name__].upsert(dict(self), ['id'])
        self.db.commit()
        return ret

    def __setitem__(self, *a, **k):
        super().__setitem__(*a, **k)
        self.Commit()
