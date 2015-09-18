from peewee import *

db = SqliteDatabase('dssl.db')

class BaseModel(Model):
    class Meta:
        database = db

class Setlist(BaseModel):
    date = DateTimeField()
    sl_type = CharField()
    sl_no = IntegerField()
    location = TextField()
    uuid = CharField(unique=True)

class Song(BaseModel):
    setlist = ForeignKeyField(Setlist, related_name="songs")
    seq = IntegerField()
    title = CharField()
    artiste = CharField()

Setlist.create_table()
Song.create_table()
