from peewee import *

database = SqliteDatabase("flux.sqlite3")


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    name = CharField()
    surname = CharField()
    email = CharField()
    password = CharField()


class Flux(BaseModel):
    link = CharField()
    user = ForeignKeyField(User, backref="user")


def create_tables():
    with database:
        database.create_tables([Flux, User])


def drop_tables():
    with database:
        database.drop_tables([Flux, User])
