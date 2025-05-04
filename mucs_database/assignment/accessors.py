import logging
from datetime import datetime

from peewee import IntegrityError

import mucs_database.assignment
from mucs_database.assignment.model import Assignment
from mucs_database.init import get_mucsv2_instance_code

logger = logging.getLogger(__name__)


def store_assignment(name: str, canvas_id: int, open_at: datetime, due_at: datetime, replace: bool = False):
    """Insert an Assignment row (or ignore if it exists)"""
    code = get_mucsv2_instance_code()
    logger.debug(f"Storing Assignment ID={canvas_id!r} name={name!r}")
    try:
        query = Assignment.insert(
            mucsv2_name=name,
            canvas_id=canvas_id,
            open_at=open_at,
            due_at=due_at,
            mucsv2_course=code, )
        if replace:
            # REPLACE the whole row
            query = query.on_conflict(action='REPLACE')
        else:
            # DO NOTHING on conflict
            query = query.on_conflict(action='IGNORE')
        query.execute()
    except IntegrityError as e:
        logger.warning(f"Assignment {name} already exists; skipping | {e}")
