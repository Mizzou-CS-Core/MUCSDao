import sqlite3
import logging
from peewee import *
from peewee import SqliteDatabase

logger = logging.getLogger(__name__)
database = Proxy()

_db: SqliteDatabase | None = None
_mucsv2_instance_code: str | None = None


def get_connection() -> SqliteDatabase:
    if _db is None:
        raise RuntimeError("Database not initialized! Call initialize_database() first.")
    return _db


def get_mucsv2_instance_code() -> str:
    if _mucsv2_instance_code is None:
        raise RuntimeError("Database not initialized! Call initialize_database() first.")
    return _mucsv2_instance_code


def initialize_database(sqlite_db_path: str, mucsv2_instance_code: str) -> None:
    global _db, _mucsv2_instance_code
    if _db is not None:
        logger.warning("Database already initialized – ignoring extra init()")
        return

    logger.debug(f"Opening SQLite DB at {sqlite_db_path!r}")
    _db = SqliteDatabase(
        sqlite_db_path,
        pragmas={
            "foreign_keys": 1,  # Enforce FK constraints
            "journal_mode": "wal",  # For concurrent writes (optional)
        },
        check_same_thread=False,
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    database.initialize(_db)
    from mucs_database.person.model import Student
    from mucs_database.canvas_course.model import CanvasCourse
    from mucs_database.assignment.model import Assignment
    from mucs_database.grading_group.model import GradingGroup
    from mucs_database.mucsv2_course.model import MUCSV2Course
    # Optional: nicer row access
    # _conn.row_factory = sqlite3.Row
    _db.connect()
    _db.create_tables([
        MUCSV2Course,
        CanvasCourse,
        GradingGroup,
        Student,
        Assignment,
    ], safe=True)

    logger.info("Database initialized and tables created")
    _mucsv2_instance_code = mucsv2_instance_code
