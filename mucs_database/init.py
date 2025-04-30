import sqlite3
import logging

logger = logging.getLogger(__name__)

_conn: sqlite3.Connection | None = None
_class_code: str | None = None


_sql_statements = [
    """CREATE TABLE IF NOT EXISTS mucsv2_course (
    course_code     TEXT    PRIMARY KEY
    );""",

    """CREATE TABLE IF NOT EXISTS canvas_course (
    canvas_id           INTEGER PRIMARY KEY,
    mucs_course_code    TEXT    NOT NULL,
    name                TEXT    NOT NULL,
    FOREIGN KEY (mucs_course_code)
        REFERENCES mucsv2_course(course_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );""",
    """CREATE TABLE IF NOT EXISTS graders (
    canvas_id           INTEGER PRIMARY KEY,
    canvas_course_id    INTEGER NOT NULL,
    name                TEXT    NOT NULL,
    FOREIGN KEY (canvas_course_id)
        REFERENCES canvas_course(canvas_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );""",
    """CREATE TABLE IF NOT EXISTS students (
    canvas_id   INTEGER PRIMARY KEY,
    grader_id   INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    pawprint    TEXT,
    FOREIGN KEY (grader_id)
        REFERENCES graders(canvas_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );""",
    """CREATE TABLE IF NOT EXISTS assignments (
    canvas_id        INTEGER NOT NULL,
    mucs_course_code TEXT    NOT NULL,
    name             TEXT PRIMARY KEY,
    open_at          DATE,
    due_at           DATE    NOT NULL,
    FOREIGN KEY (mucs_course_code)
        REFERENCES mucsv2_course(course_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );"""
]
def get_connection() -> sqlite3.Connection:
    if _conn is None:
        raise RuntimeError("Database not initialized! Call init() first.")
    return _conn
def get_class_code() -> str:
    if _class_code is None:
        raise RuntimeError("Database not initialized! Call init() first.")
    return _class_code

def initialize_database(sqlite_db_path: str, class_code: str) -> None:
    global _conn, _class_code
    if _conn is not None:
        logger.warning("Database already initialized – ignoring extra init()")
        return

    logger.debug(f"Opening SQLite DB at {sqlite_db_path!r}")
    _conn = sqlite3.connect(
        sqlite_db_path,
        detect_types=sqlite3.PARSE_DECLTYPES,
        check_same_thread=False,    # if you ever share across threads
    )
    # Optional: nicer row access
    # _conn.row_factory = sqlite3.Row
    cur = _conn.cursor()
    for stmt in _sql_statements:
        logger.debug(f"Applying schema statement:\n{stmt}")
        cur.execute(stmt)
    _conn.commit()
    logger.info("Database initialized and schema applied")
    _class_code = class_code

