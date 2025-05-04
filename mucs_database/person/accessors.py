import logging

from peewee import IntegrityError

from mucs_database.person.model import Student

logger = logging.getLogger(__name__)


def store_student(pawprint: str, name: str, sortable_name: str, canvas_id: int, grader_id: int,
                  replace: bool = True) -> str:
    """
    Insert a Student row (or ignore if it exists)
    """
    logger.debug(f"Storing Student pawprint: {pawprint}")
    try:
        query = Student.insert(
            pawprint=pawprint,
            name=name,
            sortable_name=sortable_name,
            canvas_id=canvas_id,
            grading_group=grader_id)
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
