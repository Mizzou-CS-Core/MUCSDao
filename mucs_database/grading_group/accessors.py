import datetime
import logging

from peewee import IntegrityError, DoesNotExist, fn

from mucs_database.grading_group.model import GradingGroup
from mucs_database.submission.model import Submission
from mucs_database.assignment.model import Assignment
from mucs_database.person.model import Person

logger = logging.getLogger(__name__)


def store_grading_group(canvas_id: int, name: str, course_id: int, replace: bool = True) -> int or None:
    """
    Insert a GradingGroup row to MUCSv2 DB.
    :param canvas_id: The Canvas ID of the group.
    :param name: The Canvas name of the group.
    :param course_id: The Canvas course ID associated with the group.
    :param replace: Whether the DB should replace an existing row with your queried row.
    :returns: The canvas ID associated with the grading group on success, None on failure.
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
        return None
    except Exception as e:
        logger.error(f"{e}")
        return None


def get_grading_group_by_name(grading_group_name: str) -> dict or None:
    """
    Retrieves a Grading Group based on the name.

    :returns: dict("name", "canvas_id", "last_updated")
    :param grading_group_name: The name of the GradingGroup sought.
    :raises DoesNotExist: If the grading group doesn't exist.

    """
    logger.debug(f"Retrieving grading group name = {grading_group_name}")
    try:
        grader_sql = GradingGroup.get(GradingGroup.name == grading_group_name)
        return {"name": grader_sql.name, "canvas_id": grader_sql.canvas_id, "last_updated": grader_sql.last_updated}
    except DoesNotExist:
        logger.warning(f"No grading group exists with the name {grading_group_name}")


def get_grading_groups() -> list[dict]:
    return list(GradingGroup.select().dicts())


def get_latest_submissions_from_group(assignment_id: int, grading_group_id: int) -> list:
    latest_time_subquery = (
        Submission
        .select(fn.MAX(Submission.time_submitted))
        .where(
            (Submission.person == Person.pawprint) &
            (Submission.assignment == assignment_id)
        )
    )
    query = (
        Submission.select(Submission, Person)
        .join(Person, on=(Submission.person == Person.pawprint))
        .where(
            Submission.assignment == assignment_id,
            Person.grading_group == grading_group_id,
            Submission.time_submitted == latest_time_subquery
        )
    )
    return list(query)
