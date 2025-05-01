import canvas_lms_api
import logging
import sqlite3
import datetime
from peewee import *
from mucs_database.init import get_connection, get_mucsv2_instance_code
from mucs_database.models import (
    MUCSV2Course,
    CanvasCourse,
    Grader,
    Student,
    Assignment
)
logger = logging.getLogger(__name__)


_ALLOWED_DATE_FIELDS = (
    "last_assignment_pull",
    "last_grader_pull",
    "last_student_pull"
)

def store_mucs_course():
    """Ensure there’s a MUCSV2Course row for this class_code."""
    code = get_mucsv2_instance_code()
    logger.debug(f"Ensuring MUCSV2Course[{code}] exists")
    MUCSV2Course.get_or_create(
        mucsv2_instance_code=code,
    )
def store_canvas_course(course: canvas_lms_api.Course):
    """Insert a CanvasCourse row (or ignore if exists)."""
    code = get_mucsv2_instance_code()
    logger.debug(f"Storing CanvasCourse ID={course.id!r} name={course.name!r}")
    try:
        CanvasCourse.create(canvas_id=course.id, name=course.name,mucsv2_course=code,)
    except IntegrityError:
        logger.warning(f"CanvasCourse {course.id} already exists; skipping")

def store_assignment(assignment: canvas_lms_api.Assignment):
    """Insert an Assignment row (or ignore if it exists)"""
    code = get_mucsv2_instance_code()
    logger.debug(f"Storing Assignment ID={assignment.id!r} name={assignment.name!r}")
    try:
        Assignment.create(mucsv2_name=assignment.name, canvas_id=assignment.id, open_at=assignment.unlock_at, due_at=assignment.due_at,)
    except IntegrityError:
        logger.warning(f"Assignment {assignment.name} already exists; skipping")


def get_grader_by_name(grader_name: str) -> dict() | None:
    """Retrieves a Grader based on the name"""
    """Returns: dict("name", "canvas_id", "last_updated")"""
    code = get_mucsv2_instance_code
    logger.debug(f"Retrieving grader name = {grader_name}")
    try:
        grader_sql = Grader.get(Grader.name == grader_name)
        return {"name" : grader_sql.name, "canvas_id": grader_sql.canvas_id, "last_updated": grader_sql.last_updated}
    except DoesNotExist:
        logger.warning(f"No grader exists with the name {grader_name}")




def get_cache_date_from_mucs_course(field: str) -> datetime.datetime | None:
    """
    Returns the last time a particular cache date was wrote to.  
    :param cache_date: The particular column to check. Allowed values:
        - "last_assignment_pull"
        - "last_grader_pull"
        - "last_student_pull"
    """
    if field not in _ALLOWED_DATE_FIELDS:
        raise ValueError(f"{field!r} is not one of {_ALLOWED_DATE_FIELDS}")
    code = get_class_code()
    inst = MUCSV2Course.get_or_none(MUCSV2Course.mucsv2_instance_code == code)
    if not inst:
        return None
    return getattr(inst, field)

def update_cache_date_in_mucs_course(field: str):
    """
    Updates the time a particular cache date was wrote to.  
    :param cache_date: The particular column to update. Allowed values:
        - "last_assignment_pull"
        - "last_grader_pull"
        - "last_student_pull"
    """
    if field not in _ALLOWED_DATE_FIELDS:
        raise ValueError(f"{field!r} is not one of {_ALLOWED_DATE_FIELDS}")
    code = get_class_code()
    ts = datetime.datetime.now()
    (MUCSV2Course
        .update(**{field: ts})
        .where(MUCSV2Course.mucsv2_instance_code == code)
        .execute()
    )
    logger.debug(f"Set {field} = {ts.isoformat()} for MUCSV2Course[{code}]")
