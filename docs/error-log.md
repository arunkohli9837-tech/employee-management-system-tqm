# Development Error and Problem Log

This document records actual errors and development problems
encountered during the Employee Management System project.

Only genuine errors encountered during development or testing
are recorded in this document.

---

## Error Record Format

### Error / Problem

Description of the actual problem encountered.

### Stage

Development stage where the error occurred.

### Cause

Actual root cause identified after investigation.

### Solution

Actual solution implemented to resolve the problem.

### Result

Result after applying the solution and retesting.

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

This improvement increases fault tolerance and reduces failures
caused by temporary database locking.

It directly supports Q01 - Improve Reliability.

### Result

Database operations can recover from short temporary lock conditions
instead of immediately terminating with an OperationalError.

---

## Error 2 - Invalid Backup File

### Error / Problem

An invalid SQLite file was selected for database restoration.

### Stage

Stage 5 - Automatic Backup and Recovery

### Cause

The selected file was not a valid SQLite database.

### Solution

SQLite integrity checking was added before restoration.

The system now validates the selected backup and blocks restoration
when the integrity check fails.

### TQM Relevance

This is an Error Recovery and Input Validation improvement.

It prevents an invalid backup from replacing or corrupting the active
application database.

### Result

Invalid backup files are rejected safely without replacing the
current database.