import logging

import peewee
from peewee import IntegrityError

from mucs_database.person.model import Person
from mucs_database.grading_group.model import GradingGroup

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


def get_person(pawprint: str, return_dict=True) -> dict or None or Person:
    """
        Returns a Person from the DB.
        :param pawprint: The Person's pawprint you're searching for.
        :param return_dict: Whether the function should return a dictionary or the actual ORM Model.
    """
    logger.debug(f"Getting person {pawprint}")
    try:
        person = Person.select().where(Person.pawprint == pawprint)
        logger.debug(f"Retrieving successful for {pawprint}")
        if return_dict:
            logger.debug(f"Returning a dictionary of {pawprint}")
            return person.dicts().get()
        logger.debug(f"Returning a model of {pawprint}")
        return person.get()
    except peewee.DoesNotExist as e:
        logger.warning(f"{e}")
        return None


def get_person_grading_group(pawprint: str, return_dict=True) -> dict or None or GradingGroup:
    """
    Returns a Person's Grading Group.
    :param pawprint: The Person's pawprint you're searching for.
    :param return_dict: Whether the function should return a dictionary or the actual ORM Model.
    """
    logger.debug(f"Getting {pawprint}'s grading group")
    person = get_person(pawprint=pawprint, return_dict=False)
    grading_group = person.grading_group
    if return_dict:
        return grading_group.dicts().get()
    return grading_group
