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

## Stage 1 - Project Foundation

### Objective

Create the basic desktop application structure using Python,
CustomTkinter and SQLite.

### Implemented

- Created project folder structure.
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
- Added secure password hashing.
- Enabled SQLite foreign keys.
- Enabled SQLite WAL journal mode.
- Added initial audit logging.

### TQM Relevance

The first stage establishes the foundation required for improving
system reliability.

Audit logs, error records and backup history have been included at
database level so that later reliability improvements can be measured
and demonstrated.

### Status

Completed.
## Stage 2 - Employee Management and Input Validation

### Objective

Implement core Employee Management System functionality and begin the
Q01 reliability improvement process through input validation and
controlled employee record management.

### Implemented

- Add employee functionality
- View employee records
- Search employee records
- Update employee information
- Employee deactivation
- Email validation
- Phone validation
- Salary validation
- Joining date validation
- Required field validation
- Duplicate employee code prevention
- Duplicate email prevention
- Audit logging for employee operations
- Soft delete through employee deactivation

### TQM Reliability Improvements

Input validation prevents invalid and inconsistent information from
being stored in the employee database.

Database uniqueness constraints prevent duplicate employee codes and
email addresses.

Employee records are deactivated instead of permanently deleted,
reducing the risk of accidental data loss and retaining historical
records for auditing.

Employee operations are recorded through the audit logging system.

### Status

Completed.
## Stage 3 - Role-Based Access Control

### Objective

Implement user account management and role-based access control to
prevent unauthorized access to sensitive Employee Management System
functions.

### Implemented

- Admin user role
- HR user role
- Employee user role
- User account creation
- User account editing
- Password assignment
- Password reset through user update
- User activation and deactivation
- User search
- Role-based navigation
- Restricted administrative features
- Unauthorized service-level access protection
- Self-deactivation prevention
- Administrator role protection
- Last active Administrator protection
- User management audit logging

### TQM Reliability Improvements

Role-based access control prevents unauthorized users from performing
sensitive system operations.

Administrative account protection reduces the possibility of
accidentally locking all administrators out of the system.

Inactive user accounts are retained instead of permanently deleted,
providing historical traceability.

Strong password validation reduces weak account credentials.

### Status

Completed.
## Stage 4 - Audit Logging and Traceability

### Objective

Make system audit information visible and searchable so that important
user actions and failed operations can be traced during system
operation.

### Implemented

- Audit log viewer
- User activity tracking
- Login success tracking
- Failed login tracking
- Employee operation tracking
- User account operation tracking
- Success and failure status tracking
- Audit log search
- Audit status filtering
- Audit statistics
- Role-based audit log access

### TQM Reliability Improvements

Audit logging improves traceability and accountability.

Important system operations can now be reviewed to identify who
performed an action, when the action occurred, what object was affected
and whether the operation succeeded or failed.

Failed operations are retained for investigation instead of being
silently ignored.

This supports root-cause analysis and continuous quality improvement.

### Status

Completed.
## Stage 5 - Automatic Backup and Recovery

### Objective

Protect employee management data against accidental data loss and
provide a controlled database recovery mechanism.

### Implemented

- Automatic database backup on application startup
- Manual database backup
- Backup history
- Backup file listing
- SQLite integrity validation
- Database restore
- Safety backup before restore
- Restore confirmation
- Backup success/failure tracking
- Backup audit logging
- Backup statistics

### Reliability Improvements

The system now creates an automatic database backup whenever the
application starts.

Administrators can manually create additional backups before important
operations.

Before restoring an older backup, the current database is copied into a
safety backup so that the restore process itself does not unnecessarily
increase the risk of data loss.

SQLite integrity checking prevents invalid or corrupted database files
from being restored.

### TQM Relevance

This feature directly addresses the Improve Reliability requirement by
reducing the impact of database failure, accidental data modification,
and corrupted backup files.

The backup history and audit records also provide traceability for
recovery operations.

### Status

Completed.