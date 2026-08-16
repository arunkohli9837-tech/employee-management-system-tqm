from database.database import (
    get_connection,
    record_error,
)


def get_audit_logs(
    search_text="",
    status_filter="All",
):
    """
    Retrieve audit log records.

    Search supports:
    - username
    - action
    - target type
    - target id
    - description

    Status filter:
    - All
    - Success
    - Failed
    """

    connection = get_connection()

    try:

        query = """
            SELECT
                id,
                user_id,
                username,
                action,
                target_type,
                target_id,
                description,
                status,
                created_at
            FROM audit_logs
            WHERE 1 = 1
        """

        parameters = []

        # ----------------------------------------
        # SEARCH FILTER
        # ----------------------------------------

        if search_text.strip():

            search = f"%{search_text.strip()}%"

            query += """
                AND (
                    username LIKE ?
                    OR action LIKE ?
                    OR target_type LIKE ?
                    OR target_id LIKE ?
                    OR description LIKE ?
                )
            """

            parameters.extend(
                [
                    search,
                    search,
                    search,
                    search,
                    search,
                ]
            )

        # ----------------------------------------
        # STATUS FILTER
        # ----------------------------------------

        if status_filter in (
            "Success",
            "Failed",
        ):

            query += """
                AND status = ?
            """

            parameters.append(
                status_filter
            )

        query += """
            ORDER BY id DESC
        """

        rows = connection.execute(
            query,
            parameters,
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    except Exception as error:

        record_error(
            type(error).__name__,
            str(error),
            "audit_service.get_audit_logs",
        )

        return []

    finally:
        connection.close()


def get_audit_statistics():
    """
    Return basic audit log statistics.
    """

    connection = get_connection()

    try:

        total = connection.execute(
            """
            SELECT COUNT(*)
            FROM audit_logs
            """
        ).fetchone()[0]

        successful = connection.execute(
            """
            SELECT COUNT(*)
            FROM audit_logs
            WHERE status = 'Success'
            """
        ).fetchone()[0]

        failed = connection.execute(
            """
            SELECT COUNT(*)
            FROM audit_logs
            WHERE status = 'Failed'
            """
        ).fetchone()[0]

        login_events = connection.execute(
            """
            SELECT COUNT(*)
            FROM audit_logs
            WHERE action IN (
                'LOGIN',
                'LOGIN_ATTEMPT'
            )
            """
        ).fetchone()[0]

        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "login_events": login_events,
        }

    except Exception as error:

        record_error(
            type(error).__name__,
            str(error),
            "audit_service.get_audit_statistics",
        )

        return {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "login_events": 0,
        }

    finally:
        connection.close()