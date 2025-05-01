from peewee import *
from mucs_database.init import database

class BaseModel(Model):
    class Meta:
        database = database  # will be set at runtime

class MUCSV2Course(BaseModel):
    mucsv2_instance_code = CharField(primary_key=True)
    last_assignment_pull = DateTimeField()
    last_grader_pull = DateTimeField()
    last_student_pull = DateTimeField()
class CanvasCourse(BaseModel):
    canvas_id = IntegerField(primary_key=True)
    name = TextField()
    mucsv2_course = ForeignKeyField(MUCSV2Course, backref="mucsv2_course_instance")
class Grader(BaseModel):
    canvas_id = IntegerField(primary_key=True)
    name = TextField(null = False)
    last_updated = DateTimeField()
    canvas_course = ForeignKeyField(CanvasCourse, backref="canvas_course")
class Student(BaseModel):
    pawprint = TextField(primary_key=True)
    name = TextField()
    sortable_name = TextField()
    canvas_id = IntegerField()
    grader = ForeignKeyField(Grader, backref="grader")
class Assignment(BaseModel):
    mucsv2_name = TextField(primary_key=True)
    canvas_id = IntegerField()
    open_at = DateTimeField()
    due_at = DateTimeField()
    mucsv2_course = ForeignKeyField(MUCSV2Course, backref="mucsv2_course_instance")

