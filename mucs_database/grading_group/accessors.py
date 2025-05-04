import datetime
import logging

from peewee import IntegrityError, DoesNotExist

from mucs_database.grading_group.model import GradingGroup

logger = logging.getLogger(__name__)


def store_grading_group(canvas_id: int, name: str, course_id: int, replace: bool = True) -> int:
    """
    Insert a GradingGroup row (or ignore/replace if it exists)
    """
    logger.debug(f"Storing GradingGroup ID: {canvas_id!r} name={name}")
    try:

        query = GradingGroup.insert(
            canvas_id=canvas_id,
            name=name,
            last_updated=datetime.datetime.now(),
            canvas_course=course_id)
        if replace:
            # REPLACE the whole row
            query = query.on_conflict(action='REPLACE')
        else:
            # DO NOTHING on conflict
            query = query.on_conflict(action='IGNORE')
        query.execute()
        return canvas_id
    except IntegrityError as e:
        logger.warning(f"GradingGroup {canvas_id} already exists; skipping | {e}")
    except Exception as e:
        logger.error(f"{e}")


def get_grader_by_name(grading_group_name: str) -> dict or None:
    """Retrieves a Grading Group based on the name"""
    """Returns: dict("name", "canvas_id", "last_updated")"""
    logger.debug(f"Retrieving grading group name = {grading_group_name}")
    try:
        grader_sql = GradingGroup.get(GradingGroup.name == grading_group_name)
        return {"name": grader_sql.name, "canvas_id": grader_sql.canvas_id, "last_updated": grader_sql.last_updated}
    except DoesNotExist:
        logger.warning(f"No grading group exists with the name {grading_group_name}")
