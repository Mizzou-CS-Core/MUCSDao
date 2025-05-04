import logging

from peewee import IntegrityError

from mucs_database.canvas_course.model import CanvasCourse
from mucs_database.init import get_mucsv2_instance_code

logger = logging.getLogger(__name__)


def store_canvas_course(canvas_id: int, name: str, replace: bool = False) -> int or None:
    """
    Insert a CanvasCourse row to MUCSv2 DB.
    :param canvas_id: The Canvas ID of the course.
    :param name: The Canvas name of the course.
    :param replace: Whether the DB should replace an existing row with your queried row.
    :returns: The Canvas ID of the course on success, None on failure.
    """
    code = get_mucsv2_instance_code()
    logger.debug(f"Storing CanvasCourse ID={canvas_id!r} name={name!r}")
    try:
        query = CanvasCourse.insert(
            canvas_id=canvas_id,
            name=name,
            mucsv2_course=code, )
        if replace:
            # REPLACE the whole row
            query = query.on_conflict(action='REPLACE')
        else:
            # DO NOTHING on conflict
            query = query.on_conflict(action='IGNORE')
        query.execute()
        return canvas_id
    except IntegrityError as e:
        logger.warning(f"CanvasCourse {canvas_id} already exists; skipping | {e}")
        return None
