import logging

from peewee import IntegrityError

import mucs_database.assignment
from mucs_database.assignment.model import Assignment
from mucs_database.init import get_mucsv2_instance_code

logger = logging.getLogger(__name__)


def store_assignment(assignment: mucs_database.assignment.model.Assignment, replace: bool = False):
    """Insert an Assignment row (or ignore if it exists)"""
    code = get_mucsv2_instance_code()
    logger.debug(f"Storing Assignment ID={assignment.id!r} name={assignment.name!r}")
    try:
        query = Assignment.insert(
            mucsv2_name=assignment.name,
            canvas_id=assignment.id,
            open_at=assignment.unlock_at,
            due_at=assignment.due_at,
            mucsv2_course=code, )
        if replace:
            # REPLACE the whole row
            query = query.on_conflict(action='REPLACE')
        else:
            # DO NOTHING on conflict
            query = query.on_conflict(action='IGNORE')
        query.execute()
    except IntegrityError as e:
        logger.warning(f"Assignment {assignment.name} already exists; skipping | {e}")
