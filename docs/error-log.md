# Development Error and Problem Log

This document records errors, development problems, their causes and
the solutions used during the Employee Management System project.

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

### Result

Final result after applying the solution.

---
## Error 1 - SQLite Database Locked

### Error / Problem

The application displayed the following error while running:

`sqlite3.OperationalError: database is locked`

### Stage

Stage 2 - Employee Management and Input Validation

### Cause

SQLite can temporarily lock the database when another database
connection or application process is performing a write operation.

The application originally did not provide sufficient waiting time
for a locked database to become available.

### Solution

The SQLite connection configuration was improved by adding:

- Connection timeout
- SQLite busy timeout
- Transaction rollback on failed database operations
- WAL journal mode

The application now waits for a temporarily locked database instead
of failing immediately.

### TQM Relevance

This improvement increases fault tolerance and reduces failures caused
by temporary database locking.

It directly supports Q01 - Improve Reliability.

### Result

Database operations can recover from short temporary lock conditions
instead of immediately terminating with an OperationalError.
## Error 2 - Invalid Backup File

### Problem

An invalid SQLite file was selected for database restoration.

### Expected Behaviour

The application should reject the file instead of replacing the
current database.

### Cause

The selected file was not a valid SQLite database.

### Solution

SQLite PRAGMA integrity_check was added before restoration.

The system now validates the backup and blocks restoration when the
integrity check fails.

### TQM Relevance

This is an Error Recovery and Input Validation improvement. It prevents
an invalid backup from corrupting the active application database.

### Result

Invalid backup files are rejected safely without replacing the current
database.
---

## Error 3 - Invalid Employee Input

### Problem

Invalid employee information could be entered through the
Employee Management form.

Examples included:

- Empty employee code
- Invalid employee code characters
- Invalid employee name
- Invalid email address
- Invalid phone number
- Negative salary
- Invalid salary values
- Incorrect joining date

### Stage

Stage 6 - Input Validation and Error Recovery

### Cause

The initial validation rules checked only basic requirements.
Several invalid or extreme values could still reach the
database layer.

### Solution

Stronger validation rules were implemented in the employee
service layer.

The system now validates:

- Required fields
- Employee code format
- Employee name format
- Email format
- Phone number format
- Salary range and numeric validity
- Joining date format
- Future joining dates
- Maximum field lengths

Invalid data is rejected before database insertion or update.

### TQM Relevance

This improves reliability by preventing invalid data from
entering the system.

It supports:

- Input Validation
- Defect Prevention
- Data Quality
- Reliability Improvement

### Result

Invalid employee data is rejected with a clear message and
does not modify the database.

---

## Error 4 - Database Operation Failure

### Problem

A database operation could fail because of an SQLite error,
unexpected application exception, or database constraint.

### Stage

Stage 6 - Input Validation and Error Recovery

### Cause

Database operations can fail because of:

- Database locking
- Constraint violations
- Invalid database operations
- Unexpected runtime errors

### Solution

Database operations were improved using:

- Explicit transaction rollback
- SQLite-specific error handling
- General exception handling
- Error logging
- Audit logging
- User-friendly error messages

Failed create, update and deactivate operations now
rollback the transaction before returning an error.

### TQM Relevance

This implements Error Recovery and Fault Tolerance.

The system prevents partially completed database operations
from leaving inconsistent data.

### Result

When a database operation fails, the application:

1. Rolls back the failed transaction.
2. Records the technical error.
3. Records the failed user action.
4. Shows a safe message to the user.
5. Keeps previously stored data unchanged.

---

## Error 5 - Invalid Employee Selection

### Problem

An invalid or unavailable employee ID could be supplied
during employee selection, update or deactivation.

### Stage

Stage 6 - Input Validation and Error Recovery

### Cause

Employee IDs obtained from the UI should not be assumed to
always be valid.

### Solution

Employee IDs are now checked before database operations.

The system verifies:

- ID can be converted to an integer
- ID is greater than zero
- Employee record exists
- Employee is not already inactive

Invalid selections are rejected safely.

### TQM Relevance

This prevents invalid operations and improves application
fault tolerance.

### Result

Invalid employee selections no longer cause an application
crash or unintended database operation.

---

## Stage 6 Testing Record

The following tests were performed after implementing the
validation and recovery improvements.

| Test Case | Expected Result | Status |
|---|---|---|
| Empty employee code | Reject input | Passed |
| One-character employee code | Reject input | Passed |
| Invalid employee code characters | Reject input | Passed |
| Empty employee name | Reject input | Passed |
| Name containing invalid numbers | Reject input | Passed |
| Invalid email | Reject input | Passed |
| Invalid phone number | Reject input | Passed |
| Negative salary | Reject input | Passed |
| Text entered as salary | Reject input | Passed |
| Future joining date | Reject input | Passed |
| Duplicate employee code | Reject and preserve database | Passed |
| Duplicate employee email | Reject and preserve database | Passed |
| Invalid employee ID | Reject operation safely | Passed |
| Employee not found | Show error without crash | Passed |
| Already inactive employee | Reject duplicate deactivation | Passed |
| Database failure | Rollback and log error | Passed |
| Valid employee creation | Save successfully | Passed |
| Valid employee update | Update successfully | Passed |
| Valid employee deactivation | Deactivate successfully | Passed |

### Stage 6 Result

Input validation and error recovery were successfully
implemented.

The Employee Management System now prevents invalid data,
handles database failures using transaction rollback, records
errors and failed operations, and provides user-friendly
feedback without unnecessarily terminating the application.