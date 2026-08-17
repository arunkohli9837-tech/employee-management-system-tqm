# Development Log

## Project

Employee Management System

## TQM Assignment

Q01 - Improve Reliability

## Student

Arun  
B.Tech CSE  
Section A

---

# Stage 1 - Project Foundation

## Objective

Create the basic desktop application structure using Python,
CustomTkinter and SQLite.

## Implemented

- Created project folder structure.
- Added Python virtual environment.
- Added CustomTkinter desktop UI.
- Created SQLite database.
- Added automatic database initialization.
- Added users table.
- Added employees table.
- Added audit log table.
- Added error log table.
- Added backup history table.
- Created administrator login.
- Added basic dashboard.
- Added password hashing.
- Enabled SQLite foreign keys.
- Enabled SQLite WAL journal mode.
- Added initial audit logging.

## TQM Relevance

The first stage establishes the technical foundation required
for improving system reliability.

Audit logs, error records and backup history were included at
database level so that reliability-related activities can be
recorded and reviewed.

## Status

Completed.

---

# Stage 2 - Employee Management

## Objective

Implement the core Employee Management System functionality and
establish initial reliability controls through controlled employee
record management and validation.

## Implemented

- Add employee functionality.
- View employee records.
- Search employee records.
- Update employee information.
- Employee deactivation.
- Required field validation.
- Email validation.
- Phone validation.
- Salary validation.
- Joining date validation.
- Duplicate employee code prevention.
- Duplicate email prevention.
- Employee operation audit logging.
- Soft delete through employee deactivation.

## TQM Reliability Improvements

Input validation reduces the possibility of invalid information
being stored in the employee database.

Database uniqueness constraints prevent duplicate employee codes
and email addresses.

Employee records are deactivated instead of permanently deleted.
This reduces the risk of accidental data loss and retains the
record for historical traceability.

Employee operations are recorded through the audit logging system.

## Status

Completed.

---

# Stage 3 - Role-Based Access Control

## Objective

Implement user account management and role-based access control
to prevent unauthorized access to sensitive Employee Management
System functions.

## Implemented

- Admin user role.
- HR user role.
- Employee user role.
- User account creation.
- User account editing.
- Password assignment.
- Password update/reset through user management.
- User activation and deactivation.
- User search.
- Role-based navigation.
- Restricted administrative features.
- Service-level access protection.
- Self-deactivation prevention.
- Administrator role protection.
- Last active administrator protection.
- User management audit logging.

## TQM Reliability Improvements

Role-based access control reduces the risk of unauthorized users
performing sensitive system operations.

Administrative account protection reduces the possibility of
accidentally removing access to all administrator accounts.

Inactive user accounts are retained instead of permanently deleted,
providing historical traceability.

Password validation helps prevent weak account credentials.

## Status

Completed.

---

# Stage 4 - Audit Logging and Traceability

## Objective

Make important system activities traceable so that successful
and failed operations can be reviewed during system operation.

## Implemented

- Audit log viewer.
- User activity tracking.
- Login success tracking.
- Failed login tracking.
- Employee operation tracking.
- User account operation tracking.
- Success and failure status tracking.
- Audit log search.
- Audit status filtering.
- Audit statistics.
- Role-based audit log access.

## TQM Reliability Improvements

Audit logging improves traceability and accountability.

Important system operations can be reviewed to identify:

- Who performed an action.
- When the action occurred.
- What object was affected.
- Whether the operation succeeded or failed.

Failed operations can be retained for investigation instead of
being silently ignored.

This provides evidence for root-cause analysis and supports
continuous quality improvement.

## Status

Completed.

---

# Stage 5 - Automatic Backup and Recovery

## Objective

Protect employee management data against accidental data loss
and provide a controlled database recovery mechanism.

## Implemented

- Automatic database backup on application startup.
- Manual database backup.
- Backup history.
- Backup file listing.
- SQLite backup integrity validation.
- Database restore.
- Safety backup before restore.
- Restore confirmation.
- Backup success/failure tracking.
- Backup audit logging.
- Backup statistics.

## Reliability Improvements

The system creates an automatic database backup when the
application starts.

Administrators can create additional backups before important
operations.

Before restoring an older backup, the current database is copied
into a safety backup.

This provides an additional recovery point if the restoration
process itself needs to be reversed.

SQLite integrity validation helps prevent an invalid database
file from being restored.

## TQM Relevance

This stage directly addresses Q01 - Improve Reliability by
reducing the impact of:

- Accidental data loss.
- Database corruption.
- Incorrect database restoration.
- Unplanned recovery operations.

Backup history and audit records also provide traceability for
recovery activities.

## Status

Completed.

---

# Stage 6 - Input Validation and Error Recovery

## Objective

Strengthen Employee Management System reliability by improving
input validation, controlled error handling and safe employee
operations.

## Implemented

### Input Validation

- Employee code required validation.
- Minimum employee code length validation.
- Employee name required validation.
- Minimum employee name length validation.
- Email format validation.
- Phone format validation.
- Department required validation.
- Designation required validation.
- Salary required validation.
- Numeric salary validation.
- Negative salary prevention.
- Joining date required validation.
- Joining date format validation.

### Error Handling

- SQLite integrity error handling.
- General exception handling.
- Error logging.
- Audit logging for important failed operations.
- User-friendly error messages.
- Safe database connection closing.
- Employee existence checks.
- Already-inactive employee checks.
- UI protection against invalid employee selections.

### Employee Reliability

- Duplicate employee code prevention.
- Duplicate employee email prevention.
- Employee deactivation instead of permanent deletion.
- Existing employee record verification before update.
- Existing employee verification before deactivation.

## TQM Reliability Improvements

The implementation focuses on preventing defects before they
reach the database and safely handling failures that occur during
normal application operation.

Input validation improves data quality.

Database constraints protect data integrity.

Exception handling reduces the possibility of application
termination due to expected database/application errors.

Audit logs and error logs provide traceability for investigation.

Employee deactivation provides a safer alternative to permanent
deletion and preserves historical records.

## Testing

Stage 6 testing covered:

- Required field validation.
- Email validation.
- Phone validation.
- Salary validation.
- Joining date validation.
- Duplicate employee detection.
- Employee update.
- Employee deactivation.
- Invalid employee selection.
- Already inactive employee handling.
- Valid employee creation.
- Error handling.

The application was run after the implementation and the tested
employee management operations completed without application
crashes.

## TQM Relevance

Stage 6 directly supports Q01 - Improve Reliability through:

- Input Validation.
- Defect Prevention.
- Data Integrity.
- Error Handling.
- Fault Tolerance.
- Traceability.
- Safer Record Management.

## Status

Completed.