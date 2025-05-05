import logging
from datetime import datetime

from peewee import IntegrityError, DoesNotExist

from mucs_database.assignment.model import Assignment
from mucs_database.init import get_mucsv2_instance_code

logger = logging.getLogger(__name__)


def store_assignment(name: str, canvas_id: int, open_at: datetime,
                     due_at: datetime, original_name: str, assignment_type: str, file_count: int,
                     replace: bool = False) -> str or None:
    """
    Insert an Assignment row to MUCSv2 DB
    :param name: The name of the assignment.
    :param canvas_id: The Canvas ID associated with the assignment.
    :param open_at: When the assignment can start having work submitted to it.
    :param due_at: When the assignment can no longer have work submitted to it.
    :param replace: Whether the DB should replace an existing row with your queried row.
    :returns: The name of the assignment on success, None on failure.
    """
    code = get_mucsv2_instance_code()
    logger.debug(f"Storing Assignment ID={canvas_id!r} name={name!r}")
    try:
        query = Assignment.insert(
            mucsv2_name=name,
            canvas_id=canvas_id,
            open_at=open_at,
            due_at=due_at,
            mucsv2_course=code,
            assignment_type=assignment_type,
            file_submission_count=file_count,
            original_name=original_name, )
        if replace:
            # REPLACE the whole row
            query = query.on_conflict(action='REPLACE')
        else:
            # DO NOTHING on conflict
            query = query.on_conflict(action='IGNORE')
        query.execute()
        return name
    except IntegrityError as e:
        logger.warning(f"Assignment {name} already exists; skipping | {e}")
        return None


def get_assignments() -> list[dict]:
    """
    Returns a list of assignment dicts.
    """
    logger.debug("Retrieving list of assignments from DB")
    return list(Assignment.select().dicts())


def get_assignment_by_name(name: str) -> dict or None:
    """
    Returns an assignment dependent on a name.
    :param name: The name of the assignment you're seeking.
    :returns: dict() or None if failure
    """
    logger.debug(f"Retrieving assignment corresponding to mucsv2_name: {name}")
    try:
        data: dict = (Assignment
                      .select()
                      .where(Assignment.mucsv2_name == name)
                      .dicts()
                      .get())
        logger.debug(f"Retrievement successful for {name}")
        return data
    except DoesNotExist as e:
        logger.warning(f"Assignment corresponding to mucsv2_name: {name} does not exist")
        return None
