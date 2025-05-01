from peewee import *
import datetime
from mucs_database.init import database

class BaseModel(Model):
    class Meta:
        database = database  # will be set at runtime

class MUCSV2Course(BaseModel):
    """
    :param mucsv2_instance_code: primary key
    :param last_assignment_pull:
    :param last_grader_pull:
    :param last_student_pull:
    """
    mucsv2_instance_code = CharField(primary_key=True)
    last_assignment_pull = DateTimeField(default=datetime.datetime.utcnow)
    last_grader_pull     = DateTimeField(default=datetime.datetime.utcnow)
    last_student_pull    = DateTimeField(default=datetime.datetime.utcnow)
class CanvasCourse(BaseModel):
    """
    :param canvas_id: int primary key
    :param name: text
    :param mucsv2_course: foreign key to MUCSV2Course, will accept the primary key of MUCSV2Course
    """
    canvas_id = IntegerField(primary_key=True)
    name = TextField()
    mucsv2_course = ForeignKeyField(MUCSV2Course, backref="mucsv2_course_instance")
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
class Student(BaseModel):
    """
    :param pawprint: text primary key
    :param name: text
    :param sortable_name: text
    :param canvas_id: int
    :param grader: foreign key to GradingGroup, will accept the primary key of GradingGroup
    """
    pawprint = TextField(primary_key=True)
    name = TextField()
    sortable_name = TextField()
    canvas_id = IntegerField()
    grader = ForeignKeyField(GradingGroup, backref="grader")
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

