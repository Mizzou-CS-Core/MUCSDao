from canvas_lms_api import Course, Assignment
import logging
import sqlite3
import datetime
from mucs_database.init import get_connection, get_class_code
logger = logging.getLogger(__name__)


_ALLOWED_DATE_FIELDS = (
    "last_assignment_pull",
    "last_grader_pull",
    "last_student_pull"
)
def _cursor():
    return get_connection().cursor()

def store_assignment(assignment: Assignment):
    sql = "INSERT INTO assignments(canvas_id, mucs_course_code, name, open_at, due_at) VALUES (?, ?, ?, ?, ?)"
    logger.debug(f"Storing an Assignment with Canvas ID: {assignment.id}")
    asn = (assignment.id, get_class_code(), assignment.name, assignment.unlock_at, assignment.due_at)
    cursor = _cursor()
    try:
        cursor.execute(sql, asn)
        get_connection().commit()
    except sqlite3.OperationalError as e:
        logger.error(f"Failed to insert row {asn}: {e}")
    except sqlite3.IntegrityError as e:
        logger.warning(f"Already exists! {e}")
    update_cache_date(field="last_assignment_pull")

def store_canvas_course(course: Course):
    sql = "INSERT INTO canvas_course(canvas_id, mucs_course_code, name) VALUES (?, ?, ?)"
    logger.debug(f"Storing a Course with Canvas ID: {course.id}")
    cursor = _cursor()
    row = (course.id, get_class_code(), course.name)
    try:
        cursor.execute(sql, row)
        get_connection().commit()
    except sqlite3.OperationalError as e:
        logger.error(f"Failed to insert row {row}: {e}")
def store_mucs_course():
    sql = "INSERT INTO mucsv2_course(course_code) VALUES (?)"
    logger.debug(f"Storing a MUCSv2 Course with code: {get_class_code()}")
    cursor = _cursor()
    row = (get_class_code(),)
    try:
        cursor.execute(sql, row)
        get_connection().commit()
    except sqlite3.OperationalError as e:
        logger.error(f"Failed to insert row {row}: {e}")



def get_cache_date(field: str):
    cursor = _cursor
    if field not in _ALLOWED_DATE_FIELDS:
        raise ValueError
        logger.error(f"Bad value passed! {field} is not an allowed date column.")
    sql = f"SELECT {field} FROM mucsv2_course WHERE course_code = (?)"
    row = (get_class_code(), )
    cursor.execute(sql, row)
    row = cursor.fetchone()
    if not row:
        # no such course_code (or no rows)
        return None
    date_str = row[0]
    if date_str is None:
        # column was NULL
        return None
    try:
        return datetime.datetime.fromisoformat(date_str)
    except ValueError as e:
        logger.error(f"Failed to parse date {date_str!r}: {e}")
        raise


def update_cache_date(field: str):
    cursor = _cursor
    if field not in _ALLOWED_DATE_FIELDS:
        raise ValueError
        logger.error(f"Bad value passed! {field} is not an allowed date column.")
    sql = f"UPDATE mucsv2_course SET {field} = (?) WHERE course_code = (?)"
    row = (datetime.datetime.now().isoformat(), get_class_code())
    try:
        cursor.execute(sql, row)
        get_connection().commit()
    except sqlite3.OperationalError as e:
        logger.error(f"Failed to insert row {row}: {e}")