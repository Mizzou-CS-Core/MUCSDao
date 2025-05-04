from peewee import *

from mucs_database.init import database


class BaseModel(Model):
    class Meta:
        database = database  # will be set at runtime


