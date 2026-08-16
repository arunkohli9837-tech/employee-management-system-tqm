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