# FILE LOCATION: services/employee_service.py

import math
import re
import sqlite3
from datetime import datetime

from database.database import (
    get_connection,
    record_audit_log,
    record_error,
)


EMAIL_PATTERN = (
    r"^[A-Za-z0-9._%+-]+@"
    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

PHONE_PATTERN = r"^[0-9+\-\s]{7,15}$"

EMPLOYEE_CODE_PATTERN = r"^[A-Za-z0-9_-]+$"

NAME_PATTERN = (
    r"^[A-Za-z][A-Za-z .'-]*$"
)


def validate_employee_data(data):
    """
    Validate employee form data.

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """

    employee_code = str(
        data.get("employee_code", "")
    ).strip()

    full_name = str(
        data.get("full_name", "")
    ).strip()

    email = str(
        data.get("email", "")
    ).strip()

    phone = str(
        data.get("phone", "")
    ).strip()

    department = str(
        data.get("department", "")
    ).strip()

    designation = str(
        data.get("designation", "")
    ).strip()

    salary = str(
        data.get("salary", "")
    ).strip()

    joining_date = str(
        data.get("joining_date", "")
    ).strip()

    # ---------------------------------------------
    # EMPLOYEE CODE
    # ---------------------------------------------

    if not employee_code:
        return False, "Employee code is required."

    if len(employee_code) < 2:
        return (
            False,
            "Employee code must contain at least 2 characters.",
        )

    if len(employee_code) > 30:
        return (
            False,
            "Employee code cannot exceed 30 characters.",
        )

    if not re.fullmatch(
        EMPLOYEE_CODE_PATTERN,
        employee_code,
    ):
        return (
            False,
            (
                "Employee code can contain only "
                "letters, numbers, hyphens and underscores."
            ),
        )

    # ---------------------------------------------
    # FULL NAME
    # ---------------------------------------------

    if not full_name:
        return False, "Employee name is required."

    if len(full_name) < 3:
        return (
            False,
            "Employee name must contain at least 3 characters.",
        )

    if len(full_name) > 100:
        return (
            False,
            "Employee name cannot exceed 100 characters.",
        )

    if not re.fullmatch(
        NAME_PATTERN,
        full_name,
    ):
        return (
            False,
            (
                "Employee name can contain only "
                "letters, spaces, apostrophes, dots "
                "and hyphens."
            ),
        )

    # ---------------------------------------------
    # EMAIL
    # ---------------------------------------------

    if not email:
        return False, "Email address is required."

    if len(email) > 150:
        return (
            False,
            "Email address cannot exceed 150 characters.",
        )

    if not re.fullmatch(
        EMAIL_PATTERN,
        email,
    ):
        return (
            False,
            "Please enter a valid email address.",
        )

    # ---------------------------------------------
    # PHONE
    # ---------------------------------------------

    if phone:

        if not re.fullmatch(
            PHONE_PATTERN,
            phone,
        ):
            return (
                False,
                "Please enter a valid phone number.",
            )

        digits_only = re.sub(
            r"\D",
            "",
            phone,
        )

        if len(digits_only) < 7:
            return (
                False,
                "Phone number must contain at least 7 digits.",
            )

        if len(digits_only) > 15:
            return (
                False,
                "Phone number cannot contain more than 15 digits.",
            )

    # ---------------------------------------------
    # DEPARTMENT
    # ---------------------------------------------

    if not department:
        return False, "Department is required."

    if len(department) > 100:
        return (
            False,
            "Department cannot exceed 100 characters.",
        )

    # ---------------------------------------------
    # DESIGNATION
    # ---------------------------------------------

    if not designation:
        return False, "Designation is required."

    if len(designation) > 100:
        return (
            False,
            "Designation cannot exceed 100 characters.",
        )

    # ---------------------------------------------
    # SALARY
    # ---------------------------------------------

    if not salary:
        return False, "Salary is required."

    try:

        salary_value = float(salary)

        if not math.isfinite(
            salary_value
        ):
            return (
                False,
                "Salary must be a finite number.",
            )

        if salary_value < 0:
            return (
                False,
                "Salary cannot be negative.",
            )

        if salary_value > 1000000000:
            return (
                False,
                "Salary value is too large.",
            )

    except (
        ValueError,
        TypeError,
    ):
        return (
            False,
            "Salary must be a valid number.",
        )

    # ---------------------------------------------
    # JOINING DATE
    # ---------------------------------------------

    if not joining_date:
        return False, "Joining date is required."

    try:

        parsed_date = datetime.strptime(
            joining_date,
            "%Y-%m-%d",
        ).date()

    except ValueError:

        return (
            False,
            "Joining date must be in YYYY-MM-DD format.",
        )

    if parsed_date > datetime.now().date():

        return (
            False,
            "Joining date cannot be in the future.",
        )

    return True, None


def create_employee(
    data,
    current_user,
):
    """
    Add a new employee to the database.
    """

    valid, validation_error = (
        validate_employee_data(data)
    )

    if not valid:

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "CREATE_EMPLOYEE",
            "Employee",
            None,
            validation_error,
            "Failed",
        )

        return False, validation_error

    connection = get_connection()

    try:

        cursor = connection.cursor()

        now = datetime.now().isoformat(
            timespec="seconds"
        )

        cursor.execute(
            """
            INSERT INTO employees (
                employee_code,
                full_name,
                email,
                phone,
                department,
                designation,
                salary,
                joining_date,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["employee_code"].strip(),
                data["full_name"].strip(),
                data["email"].strip().lower(),
                data["phone"].strip(),
                data["department"].strip(),
                data["designation"].strip(),
                float(data["salary"]),
                data["joining_date"].strip(),
                "Active",
                now,
                now,
            ),
        )

        employee_id = cursor.lastrowid

        connection.commit()

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "CREATE_EMPLOYEE",
            "Employee",
            str(employee_id),
            (
                f"Created employee "
                f"{data['employee_code'].strip()}."
            ),
            "Success",
        )

        return True, "Employee added successfully."

    except sqlite3.IntegrityError as error:

        connection.rollback()

        error_message = str(error).lower()

        if "employee_code" in error_message:

            message = (
                "Employee code already exists."
            )

        elif "email" in error_message:

            message = (
                "Employee email already exists."
            )

        else:

            message = (
                "Duplicate or invalid employee data."
            )

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "CREATE_EMPLOYEE",
            "Employee",
            None,
            message,
            "Failed",
        )

        return False, message

    except sqlite3.Error as error:

        connection.rollback()

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.create_employee",
        )

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "CREATE_EMPLOYEE",
            "Employee",
            None,
            str(error),
            "Failed",
        )

        return (
            False,
            (
                "Database error occurred while "
                "adding employee. No changes were saved."
            ),
        )

    except Exception as error:

        connection.rollback()

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.create_employee",
        )

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "CREATE_EMPLOYEE",
            "Employee",
            None,
            str(error),
            "Failed",
        )

        return (
            False,
            (
                "Unexpected error occurred while "
                "adding employee."
            ),
        )

    finally:

        connection.close()


def get_all_employees(
    search_text="",
):
    """
    Get all employees.

    Search can match employee code, name,
    email, department or designation.
    """

    connection = get_connection()

    try:

        search_text = str(
            search_text
        ).strip()

        if search_text:

            search = f"%{search_text}%"

            rows = connection.execute(
                """
                SELECT *
                FROM employees
                WHERE employee_code LIKE ?
                   OR full_name LIKE ?
                   OR email LIKE ?
                   OR department LIKE ?
                   OR designation LIKE ?
                ORDER BY id DESC
                """,
                (
                    search,
                    search,
                    search,
                    search,
                    search,
                ),
            ).fetchall()

        else:

            rows = connection.execute(
                """
                SELECT *
                FROM employees
                ORDER BY id DESC
                """
            ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    except sqlite3.Error as error:

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.get_all_employees",
        )

        return []

    except Exception as error:

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.get_all_employees",
        )

        return []

    finally:

        connection.close()


def get_employee_by_id(
    employee_id,
):
    """
    Get one employee by database ID.
    """

    connection = get_connection()

    try:

        try:

            employee_id = int(
                employee_id
            )

        except (
            ValueError,
            TypeError,
        ):

            return None

        if employee_id <= 0:
            return None

        row = connection.execute(
            """
            SELECT *
            FROM employees
            WHERE id = ?
            """,
            (employee_id,),
        ).fetchone()

        if row:
            return dict(row)

        return None

    except sqlite3.Error as error:

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.get_employee_by_id",
        )

        return None

    except Exception as error:

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.get_employee_by_id",
        )

        return None

    finally:

        connection.close()


def update_employee(
    employee_id,
    data,
    current_user,
):
    """
    Update existing employee.
    """

    valid, validation_error = (
        validate_employee_data(data)
    )

    if not valid:

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "UPDATE_EMPLOYEE",
            "Employee",
            str(employee_id),
            validation_error,
            "Failed",
        )

        return False, validation_error

    connection = get_connection()

    try:

        existing_employee = connection.execute(
            """
            SELECT id
            FROM employees
            WHERE id = ?
            """,
            (employee_id,),
        ).fetchone()

        if not existing_employee:

            message = "Employee not found."

            record_audit_log(
                current_user["id"],
                current_user["username"],
                "UPDATE_EMPLOYEE",
                "Employee",
                str(employee_id),
                message,
                "Failed",
            )

            return False, message

        connection.execute(
            """
            UPDATE employees
            SET
                employee_code = ?,
                full_name = ?,
                email = ?,
                phone = ?,
                department = ?,
                designation = ?,
                salary = ?,
                joining_date = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                data["employee_code"].strip(),
                data["full_name"].strip(),
                data["email"].strip().lower(),
                data["phone"].strip(),
                data["department"].strip(),
                data["designation"].strip(),
                float(data["salary"]),
                data["joining_date"].strip(),
                datetime.now().isoformat(
                    timespec="seconds"
                ),
                employee_id,
            ),
        )

        connection.commit()

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "UPDATE_EMPLOYEE",
            "Employee",
            str(employee_id),
            (
                f"Updated employee "
                f"{data['employee_code'].strip()}."
            ),
            "Success",
        )

        return True, "Employee updated successfully."

    except sqlite3.IntegrityError as error:

        connection.rollback()

        error_message = str(error).lower()

        if "employee_code" in error_message:

            message = (
                "Employee code already exists."
            )

        elif "email" in error_message:

            message = (
                "Employee email already exists."
            )

        else:

            message = (
                "Duplicate or invalid employee data."
            )

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "UPDATE_EMPLOYEE",
            "Employee",
            str(employee_id),
            message,
            "Failed",
        )

        return False, message

    except sqlite3.Error as error:

        connection.rollback()

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.update_employee",
        )

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "UPDATE_EMPLOYEE",
            "Employee",
            str(employee_id),
            str(error),
            "Failed",
        )

        return (
            False,
            (
                "Database error occurred while "
                "updating employee. No changes were saved."
            ),
        )

    except Exception as error:

        connection.rollback()

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.update_employee",
        )

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "UPDATE_EMPLOYEE",
            "Employee",
            str(employee_id),
            str(error),
            "Failed",
        )

        return (
            False,
            (
                "Unexpected error occurred while "
                "updating employee."
            ),
        )

    finally:

        connection.close()


def deactivate_employee(
    employee_id,
    current_user,
):
    """
    Deactivate employee instead of permanently deleting data.

    Soft delete improves reliability because records
    can still be retained for auditing and recovery.
    """

    connection = get_connection()

    try:

        try:

            employee_id = int(
                employee_id
            )

        except (
            ValueError,
            TypeError,
        ):

            message = (
                "Invalid employee selection."
            )

            record_audit_log(
                current_user["id"],
                current_user["username"],
                "DEACTIVATE_EMPLOYEE",
                "Employee",
                None,
                message,
                "Failed",
            )

            return False, message

        if employee_id <= 0:

            message = (
                "Invalid employee selection."
            )

            record_audit_log(
                current_user["id"],
                current_user["username"],
                "DEACTIVATE_EMPLOYEE",
                "Employee",
                str(employee_id),
                message,
                "Failed",
            )

            return False, message

        employee = connection.execute(
            """
            SELECT employee_code, status
            FROM employees
            WHERE id = ?
            """,
            (employee_id,),
        ).fetchone()

        if not employee:

            message = "Employee not found."

            record_audit_log(
                current_user["id"],
                current_user["username"],
                "DEACTIVATE_EMPLOYEE",
                "Employee",
                str(employee_id),
                message,
                "Failed",
            )

            return False, message

        if employee["status"] == "Inactive":

            message = (
                "Employee is already inactive."
            )

            record_audit_log(
                current_user["id"],
                current_user["username"],
                "DEACTIVATE_EMPLOYEE",
                "Employee",
                str(employee_id),
                message,
                "Failed",
            )

            return False, message

        connection.execute(
            """
            UPDATE employees
            SET
                status = 'Inactive',
                updated_at = ?
            WHERE id = ?
            """,
            (
                datetime.now().isoformat(
                    timespec="seconds"
                ),
                employee_id,
            ),
        )

        connection.commit()

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "DEACTIVATE_EMPLOYEE",
            "Employee",
            str(employee_id),
            (
                f"Deactivated employee "
                f"{employee['employee_code']}."
            ),
            "Success",
        )

        return (
            True,
            "Employee deactivated successfully.",
        )

    except sqlite3.Error as error:

        connection.rollback()

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.deactivate_employee",
        )

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "DEACTIVATE_EMPLOYEE",
            "Employee",
            str(employee_id),
            str(error),
            "Failed",
        )

        return (
            False,
            (
                "Database error occurred while "
                "deactivating employee. No changes were saved."
            ),
        )

    except Exception as error:

        connection.rollback()

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.deactivate_employee",
        )

        record_audit_log(
            current_user["id"],
            current_user["username"],
            "DEACTIVATE_EMPLOYEE",
            "Employee",
            str(employee_id),
            str(error),
            "Failed",
        )

        return (
            False,
            (
                "Unexpected error occurred while "
                "deactivating employee."
            ),
        )

    finally:

        connection.close()