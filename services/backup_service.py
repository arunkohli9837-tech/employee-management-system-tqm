import shutil
import sqlite3
from pathlib import Path
from datetime import datetime

from database.database import (
    DATABASE_PATH,
    get_connection,
    record_audit_log,
    record_error,
)


# -------------------------------------------------
# BACKUP DIRECTORIES
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

BACKUP_DIR = BASE_DIR / "backups"
AUTO_BACKUP_DIR = BACKUP_DIR / "automatic"
MANUAL_BACKUP_DIR = BACKUP_DIR / "manual"
SAFETY_BACKUP_DIR = BACKUP_DIR / "safety"


def ensure_backup_directories():
    """
    Create all backup directories if they do not exist.
    """

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    AUTO_BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    MANUAL_BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    SAFETY_BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def create_backup_directory(
    backup_type,
):
    """
    Return the correct directory for the requested
    backup type.
    """

    ensure_backup_directories()

    if backup_type == "Automatic":
        return AUTO_BACKUP_DIR

    if backup_type == "Manual":
        return MANUAL_BACKUP_DIR

    if backup_type == "Safety":
        return SAFETY_BACKUP_DIR

    raise ValueError(
        "Invalid backup type."
    )


def generate_backup_path(
    backup_type,
):
    """
    Generate a unique timestamp-based backup path.
    """

    directory = create_backup_directory(
        backup_type
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    filename = (
        f"employee_management_"
        f"{backup_type.lower()}_"
        f"{timestamp}.db"
    )

    return directory / filename


def record_backup_history(
    backup_file,
    backup_type,
    status,
):
    """
    Store backup operation information.
    """

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO backup_history (
                backup_file,
                backup_type,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                str(backup_file),
                backup_type,
                status,
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        connection.commit()

    except Exception as error:

        connection.rollback()

        record_error(
            type(error).__name__,
            str(error),
            "backup_service.record_backup_history",
        )

    finally:
        connection.close()


def create_database_backup(
    backup_type="Manual",
    current_user=None,
):
    """
    Create a consistent SQLite database backup.

    SQLite's backup API is used instead of simply copying
    the file so that the backup remains reliable even when
    SQLite is using WAL mode.
    """

    ensure_backup_directories()

    if not DATABASE_PATH.exists():

        message = (
            "Database file does not exist."
        )

        if current_user:

            record_audit_log(
                current_user["id"],
                current_user["username"],
                "CREATE_BACKUP",
                "Database",
                None,
                message,
                "Failed",
            )

        return False, message

    backup_path = generate_backup_path(
        backup_type
    )

    source_connection = None
    backup_connection = None

    try:

        source_connection = sqlite3.connect(
            DATABASE_PATH,
            timeout=10,
        )

        backup_connection = sqlite3.connect(
            backup_path,
            timeout=10,
        )

        source_connection.backup(
            backup_connection
        )

        backup_connection.commit()

        record_backup_history(
            backup_path,
            backup_type,
            "Success",
        )

        if current_user:

            record_audit_log(
                current_user["id"],
                current_user["username"],
                "CREATE_BACKUP",
                "Database",
                None,
                (
                    f"{backup_type} backup created: "
                    f"{backup_path.name}"
                ),
                "Success",
            )

        return (
            True,
            f"Backup created successfully:\n{backup_path}",
        )

    except Exception as error:

        if backup_path.exists():

            try:
                backup_path.unlink()
            except Exception:
                pass

        record_backup_history(
            backup_path,
            backup_type,
            "Failed",
        )

        record_error(
            type(error).__name__,
            str(error),
            "backup_service.create_database_backup",
        )

        if current_user:

            record_audit_log(
                current_user["id"],
                current_user["username"],
                "CREATE_BACKUP",
                "Database",
                None,
                str(error),
                "Failed",
            )

        return (
            False,
            f"Backup failed:\n{error}",
        )

    finally:

        if source_connection:

            source_connection.close()

        if backup_connection:

            backup_connection.close()


def create_automatic_backup():
    """
    Create an automatic backup without requiring
    user interaction.

    This function is intended to run when the application
    starts.
    """

    return create_database_backup(
        backup_type="Automatic",
        current_user=None,
    )


def get_backup_history():
    """
    Return backup history records.
    """

    connection = get_connection()

    try:

        rows = connection.execute(
            """
            SELECT
                id,
                backup_file,
                backup_type,
                status,
                created_at
            FROM backup_history
            ORDER BY id DESC
            """
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    except Exception as error:

        record_error(
            type(error).__name__,
            str(error),
            "backup_service.get_backup_history",
        )

        return []

    finally:
        connection.close()


def get_available_backups():
    """
    Return actual backup files that currently exist.
    """

    ensure_backup_directories()

    backup_files = []

    for directory in (
        AUTO_BACKUP_DIR,
        MANUAL_BACKUP_DIR,
        SAFETY_BACKUP_DIR,
    ):

        for file_path in directory.glob(
            "*.db"
        ):

            try:

                stat = file_path.stat()

                backup_files.append(
                    {
                        "path": file_path,
                        "name": file_path.name,
                        "type": (
                            "Automatic"
                            if directory == AUTO_BACKUP_DIR
                            else (
                                "Manual"
                                if directory == MANUAL_BACKUP_DIR
                                else "Safety"
                            )
                        ),
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(
                            stat.st_mtime
                        ).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }
                )

            except OSError:
                continue

    backup_files.sort(
        key=lambda item: item["modified"],
        reverse=True,
    )

    return backup_files


def create_safety_backup():
    """
    Create an emergency backup immediately before
    a restore operation.
    """

    return create_database_backup(
        backup_type="Safety",
        current_user=None,
    )


def validate_backup(
    backup_path,
):
    """
    Check whether the selected file is a valid
    SQLite database.
    """

    backup_path = Path(
        backup_path
    )

    if not backup_path.exists():

        return (
            False,
            "Selected backup file does not exist.",
        )

    try:

        connection = sqlite3.connect(
            backup_path,
            timeout=10,
        )

        result = connection.execute(
            "PRAGMA integrity_check"
        ).fetchone()

        connection.close()

        if result and result[0] == "ok":

            return True, "Backup is valid."

        return (
            False,
            "Backup failed SQLite integrity check.",
        )

    except Exception as error:

        return (
            False,
            f"Backup validation failed: {error}",
        )


def restore_database(
    backup_path,
    current_user,
):
    """
    Restore the selected database backup.

    A safety backup is created first.
    """

    if current_user["role"] != "Admin":

        return (
            False,
            "Administrator permission is required.",
        )

    backup_path = Path(
        backup_path
    )

    valid, message = validate_backup(
        backup_path
    )

    if not valid:

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "RESTORE_DATABASE",
            "Database",
            None,
            message,
            "Failed",
        )

        return False, message

    safety_success, safety_message = (
        create_safety_backup()
    )

    if not safety_success:

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "RESTORE_DATABASE",
            "Database",
            None,
            (
                "Restore blocked because "
                "safety backup failed."
            ),
            "Failed",
        )

        return (
            False,
            (
                "Restore was blocked.\n\n"
                "Safety backup could not be created."
            ),
        )

    temporary_database = (
        DATABASE_PATH.with_suffix(
            ".restore_temp.db"
        )
    )

    try:

        # Create temporary copy first.
        shutil.copy2(
            backup_path,
            temporary_database,
        )

        # Validate the copied database.
        valid, validation_message = (
            validate_backup(
                temporary_database
            )
        )

        if not valid:

            return (
                False,
                (
                    "Restore was blocked.\n\n"
                    f"{validation_message}"
                ),
            )

        # Replace current database.
        shutil.copy2(
            temporary_database,
            DATABASE_PATH,
        )

        record_backup_history(
            backup_path,
            "Restore",
            "Success",
        )

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "RESTORE_DATABASE",
            "Database",
            None,
            (
                f"Database restored from "
                f"{backup_path.name}. "
                f"Safety backup: "
                f"{safety_message}"
            ),
            "Success",
        )

        return (
            True,
            (
                "Database restored successfully.\n\n"
                "Please restart the application."
            ),
        )

    except Exception as error:

        record_error(
            type(error).__name__,
            str(error),
            "backup_service.restore_database",
        )

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "RESTORE_DATABASE",
            "Database",
            None,
            str(error),
            "Failed",
        )

        return (
            False,
            f"Database restore failed:\n{error}",
        )

    finally:

        if temporary_database.exists():

            try:
                temporary_database.unlink()
            except Exception:
                pass


def get_backup_statistics():
    """
    Return backup statistics.
    """

    connection = get_connection()

    try:

        total = connection.execute(
            """
            SELECT COUNT(*)
            FROM backup_history
            """
        ).fetchone()[0]

        successful = connection.execute(
            """
            SELECT COUNT(*)
            FROM backup_history
            WHERE status = 'Success'
            """
        ).fetchone()[0]

        failed = connection.execute(
            """
            SELECT COUNT(*)
            FROM backup_history
            WHERE status = 'Failed'
            """
        ).fetchone()[0]

        return {
            "total": total,
            "successful": successful,
            "failed": failed,
        }

    except Exception as error:

        record_error(
            type(error).__name__,
            str(error),
            "backup_service.get_backup_statistics",
        )

        return {
            "total": 0,
            "successful": 0,
            "failed": 0,
        }

    finally:
        connection.close()