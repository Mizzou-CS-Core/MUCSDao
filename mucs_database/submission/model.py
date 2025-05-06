from peewee import TextField, ForeignKeyField, BooleanField, DateTimeField

from mucs_database.person.model import Person
from mucs_database.assignment.model import Assignment
from mucs_database.base_model import BaseModel


class Submission(BaseModel):
    # peewee will handle auto ids

    """
    A model of a Submission.
    """
    person = ForeignKeyField(Person, backref="submissions")
    assignment = ForeignKeyField(Assignment, backref="submissions")
    submission_path = TextField(null=False, default="")
    is_valid = BooleanField(null=False, default=False)
    is_late = BooleanField(null=False, default=False)
    time_submitted = DateTimeField()
