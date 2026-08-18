# Reliability Test Plan

## Project

Employee Management System

## TQM Assignment

Q01 - Improve Reliability

## Student

Arun  
B.Tech CSE  
Section A

---

## 1. Purpose

This test plan is used to verify the reliability improvements
implemented in the Employee Management System.

The testing focuses on:

- Input validation
- Data integrity
- Role-based access control
- Audit logging
- Automatic backup
- Database recovery
- Error handling
- Transaction rollback
- Application stability

Only actual test results are recorded.

No artificial errors are introduced for documentation purposes.

---

## 2. Testing Approach

Each test was performed on the working desktop application.

For every test, the following were considered:

- Test case
- Test action
- Expected result
- Actual result
- Status
- Error observed, if any
- Corrective action, if required

Possible test statuses are:

- Passed
- Failed
- Blocked

---

## 3. Reliability Test Cases

| Test ID | Test Area | Test Case | Expected Result | Status |
|---|---|---|---|---|
| RT-01 | Input Validation | Empty employee code | Input rejected | Passed |
| RT-02 | Input Validation | Invalid email | Input rejected | Passed |
| RT-03 | Input Validation | Invalid phone number | Input rejected | Passed |
| RT-04 | Input Validation | Negative salary | Input rejected | Passed |
| RT-05 | Input Validation | Invalid joining date | Input rejected | Passed |
| RT-06 | Data Integrity | Duplicate employee code | Duplicate rejected | Passed |
| RT-07 | Data Integrity | Duplicate employee email | Duplicate rejected | Passed |
| RT-08 | Employee Management | Valid employee creation | Employee saved | Passed |
| RT-09 | Employee Management | Employee update | Changes saved | Passed |
| RT-10 | Employee Management | Employee deactivation | Employee becomes inactive | Passed |
| RT-11 | RBAC | Unauthorized user access | Access restricted | Passed |
| RT-12 | Audit Logging | Successful employee operation | Action logged | Passed |
| RT-13 | Audit Logging | Failed employee operation | Failure logged | Passed |
| RT-14 | Backup | Automatic startup backup | Backup created | Passed |
| RT-15 | Backup | Manual backup | Backup created | Passed |
| RT-16 | Recovery | Valid database restore | Database restored | Passed |
| RT-17 | Recovery | Invalid backup file | Restore rejected | Passed |
| RT-18 | Error Recovery | Failed database operation | Operation handled safely | Passed |
| RT-19 | Data Recovery | Safety backup before restore | Safety backup created | Passed |
| RT-20 | Application Stability | Repeated normal operations | Application remains usable | Passed |

---

## 4. Test Execution Result

All 20 reliability test cases were executed using the working
Employee Management System.

The observed results matched the expected results for all tested
cases.

Total test cases: 20

Passed: 20

Failed: 0

Blocked: 0

Additional development error encountered during Stage 7 testing: 0

---

## 5. TQM Reliability Verification

The testing verified the following Q01 reliability improvements:

### Input Validation

Invalid employee information was rejected before being stored in
the database.

### Data Integrity

Duplicate employee codes and email addresses were prevented.

### Role-Based Access Control

Restricted operations were protected according to user roles.

### Auditability

Successful and failed operations were recorded in the audit system.

### Backup and Recovery

Automatic and manual backups were verified along with database
restore and safety backup functionality.

### Error Recovery

Recovery mechanisms were tested without introducing additional
application errors during the reliability test cycle.

### Application Stability

Repeated normal operations were performed without application
failure during the recorded test cycle.

---

## 6. Error Recording

No additional development error was encountered during Stage 7
testing.

Therefore, no new error entry was added to `docs/error-log.md`.

Only genuine errors encountered during development or testing are
recorded in the error log.

---

## 7. Stage 7 Result

Stage 7 reliability testing was completed successfully.

All 20 planned reliability test cases passed during the recorded
test cycle.

The results provide practical verification that the reliability
improvements implemented for Q01 - Improve Reliability are working
as intended.