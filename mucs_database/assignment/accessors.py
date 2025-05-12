import logging
from datetime import datetime
from typing import Optional

from peewee import IntegrityError, DoesNotExist

from mucs_database.assignment.model import Assignment
from mucs_database.init import get_mucsv2_instance_code
from deprecated import deprecated

logger = logging.getLogger(__name__)


def upsert_assignment(mucsv2_name: str, canvas_id: int, open_at: Optional[datetime] = None, due_at: datetime = None,
                      original_name: Optional[str] = None, assignment_type: Optional[str] = None,
                      file_count_expected: Optional[int] = None, test_file_directory_path: Optional[str] = None,
                      submittable_to: bool = True):
    """
    Inserts or updates an Assignment row in the DB
    :param mucsv2_name: The MUCSv2 internal name of the assignment
    :param canvas_id: The Canvas ID of the assignment
    :param due_at: when the Assignment is due
    :param open_at: OPTIONAL: when the Assignment can receive submissions
    :param original_name: OPTIONAL: the Assignment name as it appears in Canvas
    :param assignment_type: OPTIONAL: The type of language the Assignment is for
    :param file_count_expected: OPTIONAL: How many files should be expected when a submission is made
    :param test_file_directory_path: OPTIONAL: The path to test files necessary for an Assignment's submission
    :param submittable_to: OPTIONAL: Whether the assignment accepts submissions
    :return:
    """
    code = get_mucsv2_instance_code()
    insert_data: dict = {
        "mucsv2_name": mucsv2_name,
        "mucsv2_course": code,
        "canvas_id": canvas_id,
        "due_at": due_at
    }
    optionals: dict = {
        "open_at": open_at,
        "original_name": original_name,
        "assignment_type": assignment_type,
        "file_count_expected": file_count_expected,
        "test_file_directory_path": test_file_directory_path,
        "submittable_to": submittable_to
    }
    insert_data.update({k: v for k, v in optionals.items() if v is not None})
    update_map = {
        getattr(Assignment, k): insert_data[k]
        for k in optionals
        if k in insert_data
    }

    upsert = (
        Assignment
        .insert(**insert_data)
        .on_conflict(
            conflict_target=[Assignment.mucsv2_name],
            action="UPDATE",
            update=update_map
        )
    )

    # 5) execute
    try:
        upsert.execute()
        return mucsv2_name
    except IntegrityError as e:
        logger.error(f"Upsert failed for Assignment {mucsv2_name!r}: {e}")
        return None
@deprecated(reason="Use upsert instead")
def store_assignment(name: str, canvas_id: int, open_at: datetime,
                     due_at: datetime, original_name: str, assignment_type: str, file_count: int,
                     replace: bool = False, test_file_directory_path: str = "",
                     submittable_to: bool = True) -> str or None:
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
            original_name=original_name,
            test_file_directory_path=test_file_directory_path,
            submittable_to=submittable_to,
        )
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
