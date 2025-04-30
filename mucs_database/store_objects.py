from canvas_lms_api import Course, Assignment
import logging
import sqlite3
from mucs_database.init import get_connection, get_class_code
logger = logging.getLogger(__name__)

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


