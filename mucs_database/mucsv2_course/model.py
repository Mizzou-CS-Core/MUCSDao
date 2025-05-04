import datetime

from peewee import CharField, DateTimeField

from mucs_database.base_model import BaseModel


class MUCSV2Course(BaseModel):
    """
    :param mucsv2_instance_code: primary key
    :param last_assignment_pull:
    :param last_grader_pull:
    :param last_student_pull:
    """
    mucsv2_instance_code = CharField(primary_key=True)
    last_assignment_pull = DateTimeField(default=datetime.datetime.utcnow)
    last_grader_pull = DateTimeField(default=datetime.datetime.utcnow)
    last_student_pull = DateTimeField(default=datetime.datetime.utcnow)
