import re
import sqlite3
from datetime import datetime

from database.database import (
    get_connection,
    record_audit_log,
    record_error,
)


EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
PHONE_PATTERN = r"^[0-9+\-\s]{7,15}$"


def validate_employee_data(data):
    """
    Validate employee form data.

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """

    employee_code = data.get("employee_code", "").strip()
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    department = data.get("department", "").strip()
    designation = data.get("designation", "").strip()
    salary = str(data.get("salary", "")).strip()
    joining_date = data.get("joining_date", "").strip()

    if not employee_code:
        return False, "Employee code is required."

    if len(employee_code) < 2:
        return False, "Employee code must contain at least 2 characters."

    if not full_name:
        return False, "Employee name is required."

    if len(full_name) < 3:
        return False, "Employee name must contain at least 3 characters."

    if not email:
        return False, "Email address is required."

    if not re.match(EMAIL_PATTERN, email):
        return False, "Please enter a valid email address."

    if phone and not re.match(PHONE_PATTERN, phone):
        return False, "Please enter a valid phone number."

    if not department:
        return False, "Department is required."

    if not designation:
        return False, "Designation is required."

    if not salary:
        return False, "Salary is required."

    try:
        salary_value = float(salary)

        if salary_value < 0:
            return False, "Salary cannot be negative."

    except ValueError:
        return False, "Salary must be a valid number."

    if not joining_date:
        return False, "Joining date is required."

    try:
        datetime.strptime(joining_date, "%Y-%m-%d")

    except ValueError:
        return False, "Joining date must be in YYYY-MM-DD format."

    return True, None


def create_employee(data, current_user):
    """
    Add a new employee to the database.
    """

    valid, validation_error = validate_employee_data(data)

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

        now = datetime.now().isoformat(timespec="seconds")

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
            f"Created employee {data['employee_code'].strip()}.",
            "Success",
        )

        return True, "Employee added successfully."

    except sqlite3.IntegrityError as error:

        error_message = str(error)

        if "employee_code" in error_message:
            message = "Employee code already exists."

        elif "email" in error_message:
            message = "Employee email already exists."

        else:
            message = "Duplicate or invalid employee data."

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

    except Exception as error:

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

        return False, "Unexpected error occurred while adding employee."

    finally:
        connection.close()


def get_all_employees(search_text=""):
    """
    Get all employees.

    Search can match employee code, name,
    email, department or designation.
    """

    connection = get_connection()

    try:

        if search_text.strip():

            search = f"%{search_text.strip()}%"

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

        return [dict(row) for row in rows]

    except Exception as error:

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.get_all_employees",
        )

        return []

    finally:
        connection.close()


def get_employee_by_id(employee_id):
    """
    Get one employee by database ID.
    """

    connection = get_connection()

    try:

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

    finally:
        connection.close()


def update_employee(employee_id, data, current_user):
    """
    Update existing employee.
    """

    valid, validation_error = validate_employee_data(data)

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
            return False, "Employee not found."

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
                datetime.now().isoformat(timespec="seconds"),
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
            f"Updated employee {data['employee_code'].strip()}.",
            "Success",
        )

        return True, "Employee updated successfully."

    except sqlite3.IntegrityError as error:

        error_message = str(error)

        if "employee_code" in error_message:
            message = "Employee code already exists."

        elif "email" in error_message:
            message = "Employee email already exists."

        else:
            message = "Duplicate or invalid employee data."

        return False, message

    except Exception as error:

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.update_employee",
        )

        return False, "Unexpected error occurred while updating employee."

    finally:
        connection.close()


def deactivate_employee(employee_id, current_user):
    """
    Deactivate employee instead of permanently deleting data.

    Soft delete improves reliability because records
    can still be retained for auditing and recovery.
    """

    connection = get_connection()

    try:

        employee = connection.execute(
            """
            SELECT employee_code, status
            FROM employees
            WHERE id = ?
            """,
            (employee_id,),
        ).fetchone()

        if not employee:
            return False, "Employee not found."

        if employee["status"] == "Inactive":
            return False, "Employee is already inactive."

        connection.execute(
            """
            UPDATE employees
            SET
                status = 'Inactive',
                updated_at = ?
            WHERE id = ?
            """,
            (
                datetime.now().isoformat(timespec="seconds"),
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
            f"Deactivated employee {employee['employee_code']}.",
            "Success",
        )

        return True, "Employee deactivated successfully."

    except Exception as error:

        record_error(
            type(error).__name__,
            str(error),
            "employee_service.deactivate_employee",
        )

        return False, "Unexpected error occurred while deactivating employee."

    finally:
        connection.close()