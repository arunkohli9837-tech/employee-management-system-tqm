import hashlib
import os
from datetime import datetime

from database.database import (
    get_connection,
    record_audit_log,
    record_error,
)


def hash_password(password, salt=None):
    """
    Hash password using PBKDF2-HMAC-SHA256.

    Returns:
        password_hash
        salt
    """

    if salt is None:
        salt = os.urandom(16).hex()

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        100000,
    ).hex()

    return password_hash, salt


def verify_password(password, stored_hash, salt):
    """
    Verify entered password against stored password hash.
    """

    entered_hash, _ = hash_password(password, salt)

    return entered_hash == stored_hash


def create_default_admin():
    """
    Create a default administrator account during
    the first application run.
    """

    connection = get_connection()

    try:
        existing_admin = connection.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            ("admin",),
        ).fetchone()

        if existing_admin:
            return

        password_hash, salt = hash_password("Admin@123")

        connection.execute(
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
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "admin",
                password_hash,
                salt,
                "System Administrator",
                "Admin",
                "Active",
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        connection.commit()

    except Exception as error:
        record_error(
            type(error).__name__,
            str(error),
            "auth_service.create_default_admin",
        )

        raise

    finally:
        connection.close()


def authenticate_user(username, password):
    """
    Authenticate user and return user information.
    """

    connection = get_connection()

    try:
        user = connection.execute(
            """
            SELECT
                id,
                username,
                password_hash,
                password_salt,
                full_name,
                role,
                status
            FROM users
            WHERE username = ?
            """,
            (username.strip(),),
        ).fetchone()

        if user is None:
            return None, "Invalid username or password."

        if user["status"] != "Active":
            return None, "This account is inactive."

        if not verify_password(
            password,
            user["password_hash"],
            user["password_salt"],
        ):
            record_audit_log(
                user["id"],
                user["username"],
                "LOGIN_ATTEMPT",
                "User",
                str(user["id"]),
                "Incorrect password entered.",
                "Failed",
            )

            return None, "Invalid username or password."

        user_data = {
            "id": user["id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "role": user["role"],
        }

        record_audit_log(
            user["id"],
            user["username"],
            "LOGIN",
            "User",
            str(user["id"]),
            "User logged into the system.",
            "Success",
        )

        return user_data, None

    except Exception as error:
        record_error(
            type(error).__name__,
            str(error),
            "auth_service.authenticate_user",
        )

        return None, "An unexpected error occurred during login."

    finally:
        connection.close()