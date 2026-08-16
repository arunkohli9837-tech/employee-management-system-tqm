import sqlite3

from database.database import (
    get_connection,
    record_audit_log,
    record_error,
)

from services.auth_service import hash_password


VALID_ROLES = (
    "Admin",
    "HR",
    "Employee",
)


def validate_user_data(data, is_update=False):
    """
    Validate user account information.
    """

    username = data.get(
        "username",
        "",
    ).strip()

    full_name = data.get(
        "full_name",
        "",
    ).strip()

    role = data.get(
        "role",
        "",
    ).strip()

    password = data.get(
        "password",
        "",
    )

    if not username:
        return False, "Username is required."

    if len(username) < 3:
        return False, "Username must contain at least 3 characters."

    if " " in username:
        return False, "Username cannot contain spaces."

    if not full_name:
        return False, "Full name is required."

    if len(full_name) < 3:
        return False, "Full name must contain at least 3 characters."

    if role not in VALID_ROLES:
        return False, "Please select a valid user role."

    # Password mandatory only while creating new account
    if not is_update:

        if not password:
            return False, "Password is required."

    if password:

        if len(password) < 8:
            return False, "Password must contain at least 8 characters."

        if not any(
            character.isupper()
            for character in password
        ):
            return False, "Password must contain an uppercase letter."

        if not any(
            character.islower()
            for character in password
        ):
            return False, "Password must contain a lowercase letter."

        if not any(
            character.isdigit()
            for character in password
        ):
            return False, "Password must contain a number."

    return True, None


def get_all_users(search_text=""):
    """
    Return all system users.
    """

    connection = get_connection()

    try:

        if search_text.strip():

            search = f"%{search_text.strip()}%"

            rows = connection.execute(
                """
                SELECT
                    id,
                    username,
                    full_name,
                    role,
                    status,
                    created_at
                FROM users
                WHERE username LIKE ?
                   OR full_name LIKE ?
                   OR role LIKE ?
                   OR status LIKE ?
                ORDER BY id DESC
                """,
                (
                    search,
                    search,
                    search,
                    search,
                ),
            ).fetchall()

        else:

            rows = connection.execute(
                """
                SELECT
                    id,
                    username,
                    full_name,
                    role,
                    status,
                    created_at
                FROM users
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
            "user_service.get_all_users",
        )

        return []

    finally:
        connection.close()


def get_user_by_id(user_id):
    """
    Return a single user.
    """

    connection = get_connection()

    try:

        row = connection.execute(
            """
            SELECT
                id,
                username,
                full_name,
                role,
                status,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        if row:
            return dict(row)

        return None

    except Exception as error:

        record_error(
            type(error).__name__,
            str(error),
            "user_service.get_user_by_id",
        )

        return None

    finally:
        connection.close()


def create_user(data, current_user):
    """
    Create a system account.

    Only an administrator should call this function.
    """

    if current_user["role"] != "Admin":

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "CREATE_USER",
            "User",
            None,
            "Unauthorized user creation attempt.",
            "Failed",
        )

        return False, "Administrator permission is required."

    valid, error_message = validate_user_data(
        data,
        is_update=False,
    )

    if not valid:

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "CREATE_USER",
            "User",
            None,
            error_message,
            "Failed",
        )

        return False, error_message

    connection = get_connection()

    try:

        password_hash, salt = hash_password(
            data["password"]
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                password_salt,
                full_name,
                role,
                status,
                created_at
            )
            VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                'Active',
                datetime('now', 'localtime')
            )
            """,
            (
                data["username"].strip(),
                password_hash,
                salt,
                data["full_name"].strip(),
                data["role"].strip(),
            ),
        )

        user_id = cursor.lastrowid

        connection.commit()

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "CREATE_USER",
            "User",
            str(user_id),
            (
                f"Created user "
                f"{data['username'].strip()} "
                f"with role {data['role']}."
            ),
            "Success",
        )

        return True, "User account created successfully."

    except sqlite3.IntegrityError:

        connection.rollback()

        message = "Username already exists."

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "CREATE_USER",
            "User",
            None,
            message,
            "Failed",
        )

        return False, message

    except Exception as error:

        connection.rollback()

        record_error(
            type(error).__name__,
            str(error),
            "user_service.create_user",
        )

        return False, "Unexpected error occurred while creating user."

    finally:
        connection.close()


def update_user(
    user_id,
    data,
    current_user,
):
    """
    Update user information.

    Password is optional during update.
    """

    if current_user["role"] != "Admin":

        return False, "Administrator permission is required."

    valid, error_message = validate_user_data(
        data,
        is_update=True,
    )

    if not valid:
        return False, error_message

    connection = get_connection()

    try:

        existing_user = connection.execute(
            """
            SELECT
                id,
                username,
                role,
                status
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        if not existing_user:
            return False, "User account not found."

        # Prevent current Admin from accidentally removing
        # their own administrative permission.
        if (
            user_id == current_user["id"]
            and data["role"] != "Admin"
        ):
            return (
                False,
                "You cannot remove your own Administrator role."
            )

        # Protect the last active Administrator.
        if (
            existing_user["role"] == "Admin"
            and data["role"] != "Admin"
            and existing_user["status"] == "Active"
        ):

            active_admin_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM users
                WHERE role = 'Admin'
                  AND status = 'Active'
                """
            ).fetchone()[0]

            if active_admin_count <= 1:

                return (
                    False,
                    "The last active Administrator role cannot be removed."
                )

        if data.get("password"):

            password_hash, salt = hash_password(
                data["password"]
            )

            connection.execute(
                """
                UPDATE users
                SET
                    username = ?,
                    full_name = ?,
                    role = ?,
                    password_hash = ?,
                    password_salt = ?
                WHERE id = ?
                """,
                (
                    data["username"].strip(),
                    data["full_name"].strip(),
                    data["role"],
                    password_hash,
                    salt,
                    user_id,
                ),
            )

        else:

            connection.execute(
                """
                UPDATE users
                SET
                    username = ?,
                    full_name = ?,
                    role = ?
                WHERE id = ?
                """,
                (
                    data["username"].strip(),
                    data["full_name"].strip(),
                    data["role"],
                    user_id,
                ),
            )

        connection.commit()

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "UPDATE_USER",
            "User",
            str(user_id),
            (
                f"Updated user "
                f"{data['username'].strip()}."
            ),
            "Success",
        )

        return True, "User account updated successfully."

    except sqlite3.IntegrityError:

        connection.rollback()

        return False, "Username already exists."

    except Exception as error:

        connection.rollback()

        record_error(
            type(error).__name__,
            str(error),
            "user_service.update_user",
        )

        return False, "Unexpected error occurred while updating user."

    finally:
        connection.close()


def toggle_user_status(
    user_id,
    current_user,
):
    """
    Activate or deactivate a user.

    Reliability controls:
    - User cannot deactivate their own account.
    - Last active Administrator cannot be deactivated.
    """

    if current_user["role"] != "Admin":

        return False, "Administrator permission is required."

    if user_id == current_user["id"]:

        return False, "You cannot deactivate your own account."

    connection = get_connection()

    try:

        user = connection.execute(
            """
            SELECT
                id,
                username,
                role,
                status
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        if not user:
            return False, "User account not found."

        if (
            user["role"] == "Admin"
            and user["status"] == "Active"
        ):

            active_admin_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM users
                WHERE role = 'Admin'
                  AND status = 'Active'
                """
            ).fetchone()[0]

            if active_admin_count <= 1:

                return (
                    False,
                    "The last active Administrator cannot be deactivated."
                )

        new_status = (
            "Inactive"
            if user["status"] == "Active"
            else "Active"
        )

        connection.execute(
            """
            UPDATE users
            SET status = ?
            WHERE id = ?
            """,
            (
                new_status,
                user_id,
            ),
        )

        connection.commit()

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "CHANGE_USER_STATUS",
            "User",
            str(user_id),
            (
                f"Changed user "
                f"{user['username']} status "
                f"to {new_status}."
            ),
            "Success",
        )

        return (
            True,
            f"User status changed to {new_status}."
        )

    except Exception as error:

        connection.rollback()

        record_error(
            type(error).__name__,
            str(error),
            "user_service.toggle_user_status",
        )

        return False, "Unable to change user status."

    finally:
        connection.close()