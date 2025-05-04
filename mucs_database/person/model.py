from peewee import TextField, IntegerField, ForeignKeyField

from mucs_database.grading_group.model import GradingGroup
from mucs_database.base_model import BaseModel


class Person(BaseModel):
    """
    :param pawprint: text primary key
    :param name: text
    :param sortable_name: text
    :param canvas_id: int
    :param grading_group: foreign key to GradingGroup, will accept the primary key of GradingGroup
    """
    pawprint = TextField(primary_key=True)
    name = TextField()
    sortable_name = TextField()
    canvas_id = IntegerField()
    grading_group = ForeignKeyField(GradingGroup, backref="grading_group")
