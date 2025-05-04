import datetime
import logging

from mucs_database.init import get_mucsv2_instance_code
from mucs_database.mucsv2_course.model import MUCSV2Course

logger = logging.getLogger(__name__)


def store_mucs_course():
    """Ensure there’s a MUCSV2Course row for this instance code."""
    code = get_mucsv2_instance_code()
    logger.debug(f"Ensuring MUCSV2Course[{code}] exists")
    MUCSV2Course.get_or_create(
        mucsv2_instance_code=code,
    )


def get_cache_date_from_mucs_course(field: str) -> datetime.datetime or None:
    """
    Returns the last time a particular cache date was wrote to.
    :param field: The particular column to check. Allowed values:
        - "last_assignment_pull"
        - "last_grader_pull"
        - "last_student_pull"
    """
    if field not in _ALLOWED_DATE_FIELDS:
        raise ValueError(f"{field!r} is not one of {_ALLOWED_DATE_FIELDS}")
    code = get_mucsv2_instance_code()
    inst = MUCSV2Course.get_or_none(MUCSV2Course.mucsv2_instance_code == code)
    if not inst:
        return None
    return getattr(inst, field)


def update_cache_date_in_mucs_course(field: str):
    """
    Updates the time a particular cache date was wrote to.
    :param field: The particular column to update. Allowed values:
        - "last_assignment_pull"
        - "last_grader_pull"
        - "last_student_pull"
    """
    if field not in _ALLOWED_DATE_FIELDS:
        raise ValueError(f"{field!r} is not one of {_ALLOWED_DATE_FIELDS}")
    code = get_mucsv2_instance_code()
    ts = datetime.datetime.now()
    (MUCSV2Course
     .update(**{field: ts})
     .where(MUCSV2Course.mucsv2_instance_code == code)
     .execute()
     )
    logger.debug(f"Set {field} = {ts.isoformat()} for MUCSV2Course[{code}]")


_ALLOWED_DATE_FIELDS = (
    "last_assignment_pull",
    "last_grader_pull",
    "last_student_pull"
)
