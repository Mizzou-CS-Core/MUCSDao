from peewee import IntegerField, TextField, ForeignKeyField

from mucs_database.base_model import BaseModel
from mucs_database.mucsv2_course.model import MUCSV2Course


class CanvasCourse(BaseModel):
    """
    :param canvas_id: int primary key
    :param name: text
    :param mucsv2_course: foreign key to MUCSV2Course, will accept the primary key of MUCSV2Course
    """
    canvas_id = IntegerField(primary_key=True)
    name = TextField()
    mucsv2_course = ForeignKeyField(MUCSV2Course, backref="mucsv2_course_instance")
