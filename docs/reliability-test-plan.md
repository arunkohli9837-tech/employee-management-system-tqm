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
- Application recovery

Only actual test results will be recorded.

No error will be added to the project documentation unless
the error is actually observed during testing.

---

## 2. Testing Approach

Each test will be performed on the working desktop application.

For every test, the following information will be recorded:

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
| RT-01 | Input Validation | Empty employee code | Input rejected | Not Tested |
| RT-02 | Input Validation | Invalid email | Input rejected | Not Tested |
| RT-03 | Input Validation | Invalid phone number | Input rejected | Not Tested |
| RT-04 | Input Validation | Negative salary | Input rejected | Not Tested |
| RT-05 | Input Validation | Invalid joining date | Input rejected | Not Tested |
| RT-06 | Data Integrity | Duplicate employee code | Duplicate rejected | Not Tested |
| RT-07 | Data Integrity | Duplicate employee email | Duplicate rejected | Not Tested |
| RT-08 | Employee Management | Valid employee creation | Employee saved | Not Tested |
| RT-09 | Employee Management | Employee update | Changes saved | Not Tested |
| RT-10 | Employee Management | Employee deactivation | Employee becomes inactive | Not Tested |
| RT-11 | RBAC | Unauthorized user access | Access restricted | Not Tested |
| RT-12 | Audit Logging | Successful employee operation | Action logged | Not Tested |
| RT-13 | Audit Logging | Failed employee operation | Failure logged | Not Tested |
| RT-14 | Backup | Automatic startup backup | Backup created | Not Tested |
| RT-15 | Backup | Manual backup | Backup created | Not Tested |
| RT-16 | Recovery | Valid database restore | Database restored | Not Tested |
| RT-17 | Recovery | Invalid backup file | Restore rejected | Not Tested |
| RT-18 | Error Recovery | Failed database operation | Operation handled safely | Not Tested |
| RT-19 | Data Recovery | Safety backup before restore | Safety backup created | Not Tested |
| RT-20 | Application Stability | Repeated normal operations | Application remains usable | Not Tested |

---

## 4. Error Recording Rule

Errors will only be documented when they are actually encountered
during development or testing.

If a test passes without producing an error, the result will be
recorded as Passed.

No artificial errors will be created for documentation purposes.

---

## 5. Test Results

Detailed actual results will be added after executing the test cases.

---

## 6. Stage Result

Stage 7 will be considered complete after the reliability test cases
have been executed and the actual results have been documented.