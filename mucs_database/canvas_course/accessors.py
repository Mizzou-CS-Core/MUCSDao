import logging

from peewee import IntegrityError

from mucs_database.canvas_course.model import CanvasCourse
from mucs_database.init import get_mucsv2_instance_code

logger = logging.getLogger(__name__)

def store_canvas_course(course: canvas_lms_api.Course, replace: bool = False):
    """Insert a CanvasCourse row (or ignore if exists)."""
    code = get_mucsv2_instance_code()
    logger.debug(f"Storing CanvasCourse ID={course.id!r} name={course.name!r}")
    try:
        query = CanvasCourse.insert(
            canvas_id=course.id,
            name=course.name,
            mucsv2_course=code,)
        if replace:
            # REPLACE the whole row
            query = query.on_conflict(action='REPLACE')
        else:
            # DO NOTHING on conflict
            query = query.on_conflict(action='IGNORE')
        query.execute()
    except IntegrityError as e:
        logger.warning(f"CanvasCourse {course.id} already exists; skipping | {e}")
