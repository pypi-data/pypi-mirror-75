import flask_dictabase

db = flask_dictabase.Dictabase(app)
app.db = db

class Channel(flask_dictabase.BaseTable):
    pass

channel = app.db.FindOne(Channel, name=channelName)
