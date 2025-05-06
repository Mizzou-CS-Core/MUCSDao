import logging
from datetime import datetime

from peewee import IntegrityError

from mucs_database.submission.model import Submission

logger = logging.getLogger(__name__)


def store_submission(person_pawprint: str, assignment_name: str, submission_path: str, is_valid: bool, is_late: bool,
                     time_submitted: datetime):
    """

    :param person_pawprint:
    :param assignment_name:
    :param submission_path:
    :param is_valid:
    :param is_late:
    :param time_submitted:
    """

    logger.debug(f"Inserting Submission for pawprint {person_pawprint} and for assignment {assignment_name}")
    try:
        query = Submission.insert(person=person_pawprint, assignment=assignment_name,
                                  submission_path=submission_path, is_valid=is_valid,
                                  is_late=is_late, time_submitted=time_submitted)
        query.execute()
    except IntegrityError as e:
        logger.warning(f"Submission error: {e}")
