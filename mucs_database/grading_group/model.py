from peewee import IntegerField, TextField, DateTimeField, ForeignKeyField

from mucs_database.base_model import BaseModel
from mucs_database.canvas_course.model import CanvasCourse


class GradingGroup(BaseModel):
    """
    :param canvas_id: primary key
    :param name: text
    :param last_updated: datetime
    :param canvas_course: foreign key to CanvasCourse, will accept the primary key of CanvasCourse
    """
    canvas_id = IntegerField(primary_key=True)
    name = TextField(null = False)
    last_updated = DateTimeField()
    canvas_course = ForeignKeyField(CanvasCourse, backref="canvas_course")
