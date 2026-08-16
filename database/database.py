import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "employee_management.db"


def get_connection():
    """
    Create and return a reliable SQLite database connection.

    Reliability improvements:
    - Connection timeout
    - Busy timeout
    - Foreign key enforcement
    - WAL journal mode
    """

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10,
    )

    connection.row_factory = sqlite3.Row

    # ---------------------------------------------
    # SQLITE RELIABILITY SETTINGS
    # ---------------------------------------------

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    connection.execute(
        "PRAGMA journal_mode = WAL"
    )

    connection.execute(
        "PRAGMA busy_timeout = 10000"
    )

    return connection


def initialize_database():
    """
    Create all required database tables if they
    do not already exist.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ---------------------------------------------
        # USERS TABLE
        # ---------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT NOT NULL UNIQUE,

                password_hash TEXT NOT NULL,

                password_salt TEXT NOT NULL,

                full_name TEXT NOT NULL,

                role TEXT NOT NULL
                    CHECK(
                        role IN (
                            'Admin',
                            'HR',
                            'Employee'
                        )
                    ),

                status TEXT NOT NULL
                    DEFAULT 'Active'
                    CHECK(
                        status IN (
                            'Active',
                            'Inactive'
                        )
                    ),

                created_at TEXT NOT NULL
            )
            """
        )

        # ---------------------------------------------
        # EMPLOYEES TABLE
        # ---------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                employee_code TEXT NOT NULL UNIQUE,

                full_name TEXT NOT NULL,

                email TEXT NOT NULL UNIQUE,

                phone TEXT,

                department TEXT,

                designation TEXT,

                salary REAL DEFAULT 0,

                joining_date TEXT,

                status TEXT NOT NULL
                    DEFAULT 'Active'
                    CHECK(
                        status IN (
                            'Active',
                            'Inactive'
                        )
                    ),

                created_at TEXT NOT NULL,

                updated_at TEXT NOT NULL
            )
            """
        )

        # ---------------------------------------------
        # AUDIT LOG TABLE
        # ---------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                username TEXT,

                action TEXT NOT NULL,

                target_type TEXT,

                target_id TEXT,

                description TEXT,

                status TEXT NOT NULL,

                created_at TEXT NOT NULL,

                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE SET NULL
            )
            """
        )

        # ---------------------------------------------
        # ERROR LOG TABLE
        # ---------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS error_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                error_type TEXT,

                error_message TEXT NOT NULL,

                module TEXT,

                resolved INTEGER NOT NULL
                    DEFAULT 0,

                created_at TEXT NOT NULL
            )
            """
        )

        # ---------------------------------------------
        # BACKUP HISTORY TABLE
        # ---------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS backup_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                backup_file TEXT NOT NULL,

                backup_type TEXT NOT NULL,

                status TEXT NOT NULL,

                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def record_audit_log(
    user_id,
    username,
    action,
    target_type=None,
    target_id=None,
    description=None,
    status="Success",
):
    """
    Store an activity in the audit log.
    """

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO audit_logs (
                user_id,
                username,
                action,
                target_type,
                target_id,
                description,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                action,
                target_type,
                target_id,
                description,
                status,
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def record_error(
    error_type,
    error_message,
    module,
):
    """
    Save application errors inside the database.
    """

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO error_logs (
                error_type,
                error_message,
                module,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                error_type,
                str(error_message),
                module,
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        connection.commit()

    except Exception:
        connection.rollback()

    finally:
        connection.close()