# Execution Evidence – verified run on the real PyTodo Pro

This run used the **unmodified** application in `app/` (SHA-256 below). Every test used a fresh temporary SQLite database.

```
Run date: 2026-11-27 18:13 +08
Python 3.13.18
Flask 3.1.3 | Werkzeug 3.1.9 | pytest 9.1.1 | SQLite 3.53.1
Linux 6.18.44-fc-v880

SHA-256 of the application under test (unmodified):
050b4ee4bb7d42f9ea835b46569185177755feee8e420f861376df4e6097f30f  app.py
bf9140338277534439b38599f5ac3ef722880cced732bba8f1f313147d466d80  helpers.py
b3df0abd178da51a58a15b67ee3f090271b04a556757b24964b5fec0688e634e  templates/base.html
b03621ad4cad3ffb538ae1f9339eb93937f5b36f95d9bd5b1bf4091b89709b6f  templates/dashboard.html
12b17334b2e70543cfad1dce2d2e1ffc3e537e80a476ed230027fe69141464e0  templates/index.html
24ab53763ff0885f4985fd38f3169e38788713d12aff216b1dcf89c68bb92652  templates/login.html
9e2fd1a9d3ba1f601b4c64346dea49df3b3181839d39b66b9b1651ce8940c4a7  templates/register.html
063d3065b87ebefb6301e456ac3d2f7e5c4e9f255832616b4cdd4039aa8ee168  templates/task_form.html
c650b33967fa54b0bd74f1f860f458626141495232f5069368c0d1fa4999a6a9  static/style.css
```

## Results

| Suite | Command | Result |
|---|---|---|
| All non-UI automated tests | `pytest -m "not ui"` | **137 run: 100 pass, 37 fail** (`pytest_all.log`, `junit_all.xml`) |
| Regression suite (non-UI part) | `pytest -m "regression and not ui"` | 48 run: 26 pass, 22 fail (`pytest_regression.log`) |
| White-box unit tests | `pytest -m unit` | 29 run: 26 pass, 3 fail (`pytest_unit.log`) |
| Statement coverage | `python tools/statement_coverage.py` | helpers.py 100%; app.py misses only lines 242, 266, 375, 481, 482 (`statement_coverage.txt`) |

Every failing test is a confirmed defect. Each failure message names its DEF-ID, and the failing set matches the catalogue exactly: `build_documents.py` reported no status differences.

Python coverage cannot measure the Selenium UI tests (AT-001..010), the manual GUI, accessibility and compatibility checks, or the Locust performance runs. Those are recorded in folders 03, 05 and 06.

## Screenshot evidence (captured from the real app with `python tools/capture_evidence.py`)

| File | Shows |
|---|---|
| `03_Special_Testing/week 3 evidence/my_tasks_desktop.png` | Task due today labelled **Overdue** (DEF-001); `<b>` tag in a title rendered as bold (DEF-007) |
| `03_Special_Testing/week 3 evidence/my_tasks_phone.png` | Urgency column cut off at 375 px (DEF-023) |
| `03_Special_Testing/week 3 evidence/dashboard_desktop.png` | Overdue counter includes the task due today (DEF-001) |
| `03_Special_Testing/week 3 evidence/register_8char_password_DEF-002.png` | 8-character password rejected (DEF-002) |
| `05_Security_Performance/week 5 evidence/werkzeug_debugger_TC-SEC-013.png` | Traceback and file paths exposed on a server error (DEF-014, DEF-008) |
| `03_Special_Testing/week 3 evidence/*_{desktop,tablet,phone}.png` | Login, Register, My Tasks, New Task and Dashboard at three viewports |

## Per-test results

| Test | Req. | Objective | Status | Defect |
|---|---|---|---|---|
| TC-API-001 | F01 | Register valid user | Pass |  |
| TC-API-002 | F01 | Short username rejected | Pass |  |
| TC-API-003 | F01 | Short password rejected | Pass |  |
| TC-API-004 | F01 | Missing fields rejected | Pass |  |
| TC-API-005 | F01 | Duplicate username rejected | Fail | DEF-004 |
| TC-API-006 | F01 | Number as username rejected cleanly | Fail | DEF-018 |
| TC-API-007 | F02 | Login valid | Pass |  |
| TC-API-008 | F02 | Wrong password | Pass |  |
| TC-API-009 | F02 | Unknown user | Pass |  |
| TC-API-010 | F03 | Task list needs login | Pass |  |
| TC-API-011 | F12 | Categories need login (README: all except register/login) | Fail | DEF-016 |
| TC-API-012 | F12 | Categories listed when logged in | Pass |  |
| TC-API-013 | F04 | Create task with all fields | Pass |  |
| TC-API-014 | F04 | Create task with title only | Pass |  |
| TC-API-015 | F04 | Missing title rejected | Pass |  |
| TC-API-016 | F04 | Number as title handled cleanly | Fail | DEF-018 |
| TC-API-017 | F04 | Impossible date rejected | Fail | DEF-008 |
| TC-API-018 | F04 | Wrong date format rejected | Fail | DEF-008 |
| TC-API-019 | F04 | Unknown category id rejected | Fail | DEF-011 |
| TC-API-020 | F04 | Non-JSON body gets a clear error | Fail | DEF-017 |
| TC-API-021 | F04 | Very long title limited | Fail | DEF-013 |
| TC-API-022 | F05 | Get own task by id | Pass |  |
| TC-API-023 | F05 | Unknown id | Pass |  |
| TC-API-024 | F03 | Other user's task hidden | Pass |  |
| TC-API-025 | F05 | List newest first | Pass |  |
| TC-API-026 | F05 | page=0, per_page=2 returns 2 | Pass |  |
| TC-API-027 | F05 | Negative page rejected | Fail | DEF-012 |
| TC-API-028 | F05 | per_page=0 rejected | Fail | DEF-012 |
| TC-API-029 | F05 | Page beyond end returns empty list | Pass |  |
| TC-API-030 | F09 | Category filter | Pass |  |
| TC-API-031 | F09 | Status done filter | Pass |  |
| TC-API-032 | F09 | Search partial title | Pass |  |
| TC-API-033 | F09 | Search with an apostrophe works like the web UI | Fail | DEF-006 |
| TC-API-034 | F06 | PUT title only | Pass |  |
| TC-API-035 | F06 | PUT empty title rejected | Fail | DEF-009 |
| TC-API-036 | F07 | done='false' (string) not treated as true | Fail | DEF-010 |
| TC-API-037 | F03 | PUT other user's task refused | Pass |  |
| TC-API-038 | F06 | PUT unknown id | Pass |  |
| TC-API-039 | F06 | PUT impossible date rejected | Fail | DEF-008 |
| TC-API-040 | F08 | Delete own task | Pass |  |
| TC-API-041 | F08 | Delete unknown id returns 404 | Fail | DEF-005 |
| TC-API-042 | F03 | Cannot delete another user's task | Fail | DEF-005 |
| TC-API-043 | F08 | Delete needs login | Pass |  |
| TC-API-044 | F11 | Dashboard counts | Pass |  |
| TC-API-045 | F11 | Task due today not counted as overdue | Fail | DEF-001 |
| TC-API-046 | F11 | Dashboard needs login | Pass |  |
| TC-BB-001 | F01 | Username of 2 chars (below min) rejected | Pass |  |
| TC-BB-002 | F01 | Username of 3 chars (min) accepted | Pass |  |
| TC-BB-003 | F01 | Username of 4 chars accepted | Pass |  |
| TC-BB-004 | F01 | Username of 19 chars accepted | Pass |  |
| TC-BB-005 | F01 | Username of 20 chars (max) accepted | Pass |  |
| TC-BB-006 | F01 | Username of 21 chars (above max) rejected | Pass |  |
| TC-BB-007 | F01 | Username containing a space rejected | Pass |  |
| TC-BB-008 | F01 | Username containing a symbol rejected | Pass |  |
| TC-BB-009 | F01 | Password of 7 chars rejected | Pass |  |
| TC-BB-010 | F01 | Password of exactly 8 chars accepted | Fail | DEF-002 |
| TC-BB-011 | F01 | Password of 9 chars accepted | Pass |  |
| TC-BB-012 | F01 | Empty password rejected (server) | Pass |  |
| TC-BB-013 | F01 | Valid, new username + valid password creates account | Pass |  |
| TC-BB-014 | F01 | Taken username is refused | Fail | DEF-004 |
| TC-BB-015 | F01 | Valid username + invalid password -> password error | Pass |  |
| TC-BB-016 | F01 | Invalid username -> username error | Pass |  |
| TC-BB-017 | F02 | Existing user + correct password logs in | Pass |  |
| TC-BB-018 | F02 | Existing user + wrong password refused | Pass |  |
| TC-BB-019 | F02 | Unknown user refused | Pass |  |
| TC-BB-020 | F02 | Second account with same name can log in (or is refused) | Fail | DEF-004 |
| TC-BB-021 | F04 | Task with title, category and valid due date created | Pass |  |
| TC-BB-022 | F04 | Task with title only created | Pass |  |
| TC-BB-023 | F04 | Title of spaces only is refused (server) | Fail | DEF-009 |
| TC-BB-024 | F04 | Special characters shown as text | Fail | DEF-007 |
| TC-BB-025 | F10 | Yesterday -> Overdue | Pass |  |
| TC-BB-026 | F10 | Today -> Due Today | Fail | DEF-001 |
| TC-BB-027 | F10 | Tomorrow -> Due Soon | Pass |  |
| TC-BB-028 | F10 | Day 2 -> Due Soon | Pass |  |
| TC-BB-029 | F10 | Day 3 -> Upcoming | Pass |  |
| TC-BB-030 | F10 | No due date -> 'No due date' | Pass |  |
| TC-BB-031 | F10 | Completed task -> 'Done' | Pass |  |
| TC-BB-032 | F07 | Toggle open task completes it and sets completed_at | Pass |  |
| TC-BB-033 | F07 | Toggle done task reopens it and clears completed_at | Pass |  |
| TC-BB-034 | F08 | Owner deletes task | Pass |  |
| TC-BB-035 | F07 | Toggling a deleted task is refused safely | Pass |  |
| TC-BB-036 | F06 | Editing a deleted task is refused safely | Pass |  |
| TC-BB-037 | F03 | Logged-out user opening a protected page is redirected | Pass |  |
| TC-BB-038 | F02 | After logout, protected page needs login again | Pass |  |
| TC-BB-039 | F09 | Category filter shows only that category | Pass |  |
| TC-BB-040 | F09 | Status filter shows only done / only open tasks | Pass |  |
| TC-BB-041 | F09 | Search matches part of the title | Pass |  |
| TC-BB-042 | F09 | Search with no match shows empty state | Pass |  |
| TC-BB-043 | F09 | Category + search combined | Pass |  |
| TC-BB-044 | F09 | Search containing an apostrophe works in web UI | Pass |  |
| TC-BB-045 | F11 | Dashboard counters match seeded data | Pass |  |
| TC-BB-046 | F11 | Task due today is not counted as Overdue | Fail | DEF-001 |
| TC-BB-047 | F06 | Edit title, category and due date | Pass |  |
| TC-BB-048 | F06 | Edit to a title of spaces is refused | Fail | DEF-009 |
| TC-BB-049 | F04 | Impossible date is refused | Fail | DEF-008 |
| TC-SEC-001 | F02 | Session cookie is HttpOnly | Pass |  |
| TC-SEC-002 | F03 | Cookie signed with a wrong key is rejected | Pass |  |
| TC-SEC-003 | F03 | Cookie cannot be forged from source code | Fail | DEF-014 |
| TC-SEC-004 | F02 | Repeated failed logins are limited | Fail | DEF-019 |
| TC-SEC-005 | F02 | Cookie invalid after logout | Fail | DEF-020 |
| TC-SEC-006 | F08 | State-changing form needs a CSRF token | Fail | DEF-015 |
| TC-SEC-007 | F03 | PUT other user's task refused | Pass |  |
| TC-SEC-008 | F03 | DELETE other user's task refused | Fail | DEF-005 |
| TC-SEC-009 | F03 | GET other user's task refused | Pass |  |
| TC-SEC-010 | F09 | Search input cannot change the SQL query | Fail | DEF-006 |
| TC-SEC-011 | F01 | Passwords stored hashed | Pass |  |
| TC-SEC-012 | F05 | Script in title is escaped | Fail | DEF-007 |
| TC-SEC-014 | F03 | Edit page of another user's task refused | Pass |  |
| TC-WB-001 | F10 | No due date | Pass |  |
| TC-WB-002 | F10 | today defaulted (None) branch | Pass |  |
| TC-WB-003 | F10 | Past date | Pass |  |
| TC-WB-004 | F10 | Due today | Fail | DEF-001 |
| TC-WB-005 | F10 | 1 day away | Pass |  |
| TC-WB-006 | F10 | 2 days away | Pass |  |
| TC-WB-007 | F10 | 3 days away | Pass |  |
| TC-WB-008 | F10 | Characterise invalid stored date | Pass |  |
| TC-WB-009 | F01 | is_valid_password 7 chars | Pass |  |
| TC-WB-010 | F01 | is_valid_password 8 chars | Fail | DEF-002 |
| TC-WB-011 | F01 | is_valid_password 9 chars | Pass |  |
| TC-WB-012 | F01 | is_valid_password empty or non-string | Pass |  |
| TC-WB-013 | F01 | is_valid_username 2 chars or non-string | Pass |  |
| TC-WB-014 | F01 | is_valid_username 3 chars | Pass |  |
| TC-WB-015 | F01 | is_valid_username 20 chars | Pass |  |
| TC-WB-016 | F01 | is_valid_username 21 chars | Pass |  |
| TC-WB-017 | F01 | is_valid_username with symbol | Pass |  |
| TC-WB-018 | F01 | is_valid_username letters, digits, _ | Pass |  |
| TC-WB-019 | F11 | Not completed | Pass |  |
| TC-WB-020 | F11 | Completed 3 days ago | Pass |  |
| TC-WB-021 | F11 | Completed exactly 7 days ago | Fail | DEF-003 |
| TC-WB-022 | F11 | Completed 8 days ago | Pass |  |
| TC-WB-023 | F11 | Completed in the future (clock skew) | Pass |  |
| TC-WB-024 | F11 | Completed 6 days ago | Pass |  |
| TC-WB-025 | F11 | n=1, completed 2 hours ago | Pass |  |
| TC-WB-026 | F07 | done=true sets completed_at | Pass |  |
| TC-WB-027 | F07 | done=false clears completed_at | Pass |  |
| TC-WB-028 | F07 | Update without done keeps completed_at | Pass |  |
| TC-WB-029 | F07 | Completing a done task keeps it done | Pass |  |
