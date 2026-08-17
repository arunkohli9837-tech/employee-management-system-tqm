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