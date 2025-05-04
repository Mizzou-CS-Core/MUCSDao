from peewee import TextField, IntegerField, DateTimeField, ForeignKeyField

from mucs_database.base_model import BaseModel
from mucs_database.mucsv2_course.model import MUCSV2Course


class Assignment(BaseModel):
    """
    :param mucsv2_name: text primary key
    :param canvas_id: int
    :param open_at: datetime
    :param due_at: datetime
    :param mucsv2_course: foreign key to MUCSV2Course, will accept the primary key of MUCSV2Course
    """
    mucsv2_name = TextField(primary_key=True)
    canvas_id = IntegerField()
    open_at = DateTimeField()
    due_at = DateTimeField()
    mucsv2_course = ForeignKeyField(MUCSV2Course, backref="mucsv2_course_instance")
