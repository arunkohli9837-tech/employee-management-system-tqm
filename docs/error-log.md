# Development Error and Problem Log

This document records errors, development problems, their causes and
the solutions implemented during the Employee Management System project.

The purpose of this log is to maintain development traceability and
provide evidence of corrective actions taken under Q01 - Improve Reliability.

---

## Error Record Format

### Error / Problem

Description of the problem.

### Stage

Development stage where the problem occurred.

### Cause

Root cause of the problem.

### Solution

How the problem was solved.

### TQM Relevance

How the corrective action contributes to reliability and quality.

### Result

Final result after applying the solution.

---

# Error 1 - SQLite Database Locked

## Error / Problem

The application displayed the following error while running:

`sqlite3.OperationalError: database is locked`

## Stage

Stage 2 - Employee Management and Input Validation

## Cause

SQLite can temporarily lock the database when another database
connection or application process is performing a write operation.

The application originally did not provide sufficient waiting time
for a locked database to become available.

## Solution

The SQLite connection configuration was improved by adding:

- Connection timeout
- SQLite busy timeout
- WAL journal mode
- Transaction rollback support for database initialization
- Safe exception handling around database operations

The application now waits for a temporarily locked database instead
of immediately failing.

## TQM Relevance

This improves fault tolerance and reduces failures caused by
temporary database locking.

It directly supports Q01 - Improve Reliability.

## Result

The application can tolerate short temporary database lock
conditions more effectively instead of immediately terminating
with a database lock error.

---

# Error 2 - Invalid Backup File

## Error / Problem

An invalid SQLite database file could be selected during the
database restoration process.

## Stage

Stage 5 - Automatic Backup and Recovery

## Cause

A backup file may be damaged, incomplete, or may not actually be
a valid SQLite database.

Restoring such a file could potentially damage the active database.

## Solution

SQLite database integrity validation was implemented before
restoration.

The restoration process checks the selected backup before replacing
the active database.

The system also creates a safety backup of the current database
before performing a restore operation.

## TQM Relevance

This is an Error Recovery and Input Validation improvement.

It reduces the risk of data loss caused by invalid or corrupted
backup files.

## Result

Invalid backup files are rejected safely and the active database
is protected from an unsafe restoration.

---

# Error 3 - Invalid Employee Input

## Error / Problem

Invalid employee information could be entered through the
Employee Management form.

Examples include:

- Empty employee code
- Employee code that is too short
- Empty employee name
- Employee name that is too short
- Invalid email address
- Invalid phone number
- Negative salary
- Non-numeric salary
- Empty department
- Empty designation
- Empty salary
- Missing joining date
- Incorrect joining date format

## Stage

Stage 6 - Input Validation and Error Recovery

## Cause

The initial Employee Management implementation did not provide
sufficient validation for all important employee fields.

Invalid values could potentially reach the database layer.

## Solution

Validation was implemented in the employee service layer.

The system now validates:

- Employee code presence
- Minimum employee code length
- Employee name presence
- Minimum employee name length
- Email format
- Phone number format when supplied
- Department presence
- Designation presence
- Salary presence
- Numeric salary value
- Negative salary values
- Joining date presence
- Joining date format

Invalid information is rejected before the database operation
is performed.

## TQM Relevance

This supports:

- Input Validation
- Defect Prevention
- Data Quality
- Reliability Improvement

Preventing invalid data at the application layer reduces the
possibility of inconsistent employee records.

## Result

Invalid employee data is rejected with a clear validation message
and is not inserted or updated in the database.

---

# Error 4 - Duplicate Employee Data

## Error / Problem

An employee could not be added if the employee code or email
already existed in the database.

Without controlled handling, a database uniqueness error could
result in an unclear application failure.

## Stage

Stage 6 - Input Validation and Error Recovery

## Cause

The database uses unique constraints for:

- Employee code
- Employee email

Attempting to insert duplicate values produces an SQLite
integrity error.

## Solution

The employee service catches `sqlite3.IntegrityError`.

The system identifies duplicate employee code and duplicate
email conditions and returns a user-friendly message.

Examples:

`Employee code already exists.`

`Employee email already exists.`

The failed operation is also recorded in the audit log.

## TQM Relevance

This improves data integrity and provides controlled error handling
for database constraint violations.

## Result

Duplicate employee records are rejected without creating a
duplicate database record.

---

# Error 5 - Database Operation Failure

## Error / Problem

Database operations may fail because of database errors,
constraint violations, locking conditions, or unexpected
runtime exceptions.

## Stage

Stage 6 - Input Validation and Error Recovery

## Cause

Database operations depend on the availability and integrity
of the SQLite database.

Unexpected exceptions can occur during create, read, update,
or deactivate operations.

## Solution

Database operations were protected using exception handling.

The system now uses:

- SQLite-specific exception handling
- General exception handling
- Database error logging
- Audit logging for important employee operations
- User-friendly error messages
- Safe connection closing using `finally`

Unexpected errors are recorded in the `error_logs` table.

Failed employee operations are also recorded in the audit log
where applicable.

## TQM Relevance

This supports:

- Error Recovery
- Fault Tolerance
- Traceability
- Root-Cause Analysis

Technical errors are retained for investigation instead of
being silently ignored.

## Result

Unexpected database/application failures are handled without
unnecessarily terminating the application, and relevant errors
can be investigated using the error and audit logs.

---

# Error 6 - Invalid or Missing Employee Selection

## Error / Problem

An employee operation such as update or deactivation requires
a valid employee record to be selected.

An employee ID may become invalid if the record does not exist
or if the selected database record is unavailable.

## Stage

Stage 6 - Input Validation and Error Recovery

## Cause

The UI selection cannot be assumed to always represent a valid
database record.

## Solution

The application now checks the selected employee ID and attempts
to retrieve the corresponding employee record before performing
the operation.

The service layer also checks whether the employee exists.

For deactivation, the system additionally checks whether the
employee is already inactive.

## TQM Relevance

This prevents invalid employee operations and improves application
fault tolerance.

## Result

Invalid or unavailable employee selections are rejected safely
with an appropriate message instead of causing an application crash.

---

# Stage 6 Testing Record

The following test cases were used to verify the implemented
input validation and employee management reliability controls.

| Test Case | Expected Result | Status |
|---|---|---|
| Empty employee code | Reject input | Verified |
| One-character employee code | Reject input | Verified |
| Empty employee name | Reject input | Verified |
| Short employee name | Reject input | Verified |
| Invalid email | Reject input | Verified |
| Invalid phone number | Reject input | Verified |
| Empty department | Reject input | Verified |
| Empty designation | Reject input | Verified |
| Empty salary | Reject input | Verified |
| Text entered as salary | Reject input | Verified |
| Negative salary | Reject input | Verified |
| Missing joining date | Reject input | Verified |
| Incorrect joining date format | Reject input | Verified |
| Duplicate employee code | Reject operation | Verified |
| Duplicate employee email | Reject operation | Verified |
| Employee not found | Reject operation safely | Verified |
| Already inactive employee | Reject duplicate deactivation | Verified |
| Valid employee creation | Save successfully | Verified |
| Valid employee update | Update successfully | Verified |
| Valid employee deactivation | Deactivate successfully | Verified |

> Note: Testing status is based on the validation and employee
> management tests performed during Stage 6. Additional stress,
> recovery and performance measurements will be documented in
> later TQM stages.

---

# Stage 6 Result

Input validation and employee-operation error handling were
successfully implemented.

The Employee Management System now:

- Rejects invalid employee information.
- Prevents duplicate employee codes and email addresses.
- Handles database constraint errors.
- Records important employee operations through audit logging.
- Records unexpected application/database errors.
- Safely handles invalid employee selections.
- Uses employee deactivation instead of permanent deletion.
- Provides user-friendly error messages.

These improvements directly contribute to Q01 - Improve Reliability
through input validation, data integrity, fault handling and
traceability.