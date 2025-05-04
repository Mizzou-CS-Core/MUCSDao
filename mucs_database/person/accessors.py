import logging

from peewee import IntegrityError

from mucs_database.person.model import Person

logger = logging.getLogger(__name__)


def store_person(pawprint: str, name: str, sortable_name: str, canvas_id: int, grading_group_id: int,
                 replace: bool = True) -> str or None:
    """
    Insert a Person row to MUCSv2 DB
    :param pawprint: The pawprint of the person. (In Canvas, this is the "login_id".)
    :param name: The Canvas name of the person.
    :param sortable_name: The Canvas sortable name of the person.
    :param canvas_id: The Canvas ID of the person.
    :param grading_group_id: The grading group ID that the person belongs to.
    :param replace: Whether the DB should replace an existing row with your queried row.
    :returns: The pawprint of the person on success, None on failure.
    """
    logger.debug(f"Storing Student pawprint: {pawprint}")
    try:
        query = Person.insert(
            pawprint=pawprint,
            name=name,
            sortable_name=sortable_name,
            canvas_id=canvas_id,
            grading_group=grading_group_id)
        if replace:
            # REPLACE the whole row
            query = query.on_conflict(action='REPLACE')
        else:
            # DO NOTHING on conflict
            query = query.on_conflict(action='IGNORE')
        query.execute()
        return pawprint
    except IntegrityError as e:
        logger.warning(f"Student {pawprint} already exists; skipping | {e}")
        return None
