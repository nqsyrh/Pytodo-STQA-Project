# Defect Reports (all confirmed defects)

Defect Report Template from the brief. Lifecycle used: New -> Confirmed (reproduced by a second member). As an independent QA team we do not fix code, so Retest/Closed happen after the developers fix a defect (run `pytest -m regression`).
| Severity | Count |
|---|---|
| Critical | 5 |
| Major | 5 |
| Moderate | 7 |
| Minor | 9 |

## DEF-001: Task due today is labelled 'Overdue' instead of 'Due Today'

| Field | Value |
|---|---|
| Affected Feature | F10 Urgency / F11 Dashboard |
| Area | Business logic |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Logged in |
| Steps to Reproduce | 1. Create task due today 2. Open My Tasks 3. Open Dashboard |
| Expected Result | Badge 'Due Today'; Overdue counter 0 |
| Actual Result | Badge 'Overdue'; Overdue = 1 (helpers.compute_urgency uses due <= today) |
| Severity | Major |
| Priority | High |
| Evidence | TC-BB-026, TC-BB-046, TC-WB-004, TC-API-045, TC-GUI-008, AT-004 |
| Status | Confirmed |

## DEF-002: Password of exactly 8 characters is rejected

| Field | Value |
|---|---|
| Affected Feature | F01 Registration |
| Area | Input validation |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Logged out |
| Steps to Reproduce | 1. Register with password 'Abcd123!' (8 chars) |
| Expected Result | Account created |
| Actual Result | 'Password must be at least 8 characters.' (is_valid_password uses len > 8) |
| Severity | Major |
| Priority | High |
| Evidence | TC-BB-010, TC-WB-010, AT-002 |
| Status | Confirmed |

## DEF-003: Task completed exactly 7 days ago is not counted in 'Completed (last 7 days)'

| Field | Value |
|---|---|
| Affected Feature | F11 Dashboard |
| Area | Business logic |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Task completed exactly 7 days ago |
| Steps to Reproduce | 1. Call completed_in_last_n_days with age 7 days 2. Compare with dashboard |
| Expected Result | Counted (inclusive window) |
| Actual Result | Not counted (age.days < n) |
| Severity | Moderate |
| Priority | Medium |
| Evidence | TC-WB-021 |
| Status | Confirmed |

## DEF-004: Duplicate usernames are accepted; the second account can never log in

| Field | Value |
|---|---|
| Affected Feature | F01 Registration / F02 Login |
| Area | Input validation |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | 'dt_taken' exists |
| Steps to Reproduce | 1. Register 'dt_taken' again 2. Log in with second password |
| Expected Result | Refused with 'username already taken' |
| Actual Result | Second account created (302 / 201); it can never log in |
| Severity | Major |
| Priority | High |
| Evidence | TC-BB-014, TC-BB-020, TC-API-005 |
| Status | Confirmed |

## DEF-005: Any logged-in user can delete another user's task through the API

| Field | Value |
|---|---|
| Affected Feature | F08 Delete / F03 Access control |
| Area | Security |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | qa_user2 owns a task |
| Steps to Reproduce | 1. Log in as qa_user1 2. DELETE /api/tasks/<qa_user2 task id> 3. qa_user2 opens the task |
| Expected Result | 404/403; task kept. Unknown id gives 404 |
| Actual Result | 200 {'result':'ok'}; qa_user2's task is gone. Unknown id also gives 200 |
| Severity | Critical |
| Priority | High |
| Evidence | TC-API-041, TC-API-042, TC-SEC-008 |
| Status | Confirmed |

## DEF-006: SQL injection in API search parameter q leaks other users' tasks

| Field | Value |
|---|---|
| Affected Feature | F09 Search |
| Area | Security |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | qa_user1 and qa_user2 each own a task |
| Steps to Reproduce | 1. Log in as qa_user1 2. GET /api/tasks?q=x%' OR user_id != 0 OR title LIKE '% 3. GET /api/tasks?q=Mum's |
| Expected Result | Only own tasks; apostrophe search works |
| Actual Result | qa_user2's task returned; apostrophe gives HTTP 500 |
| Severity | Critical |
| Priority | High |
| Evidence | TC-SEC-010, TC-API-033 |
| Status | Confirmed |

## DEF-007: Task title is rendered as raw HTML (stored XSS)

| Field | Value |
|---|---|
| Affected Feature | F04 Create / F05 List |
| Area | Security |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Logged in |
| Steps to Reproduce | 1. Create task titled <script>alert(1)</script> 2. Open My Tasks |
| Expected Result | Title shown as text |
| Actual Result | Script tag rendered (template uses \|safe) |
| Severity | Critical |
| Priority | High |
| Evidence | TC-BB-024, TC-SEC-012, AT-008 |
| Status | Confirmed |

## DEF-008: Invalid due date is saved and then breaks My Tasks, the API list and the Dashboard (HTTP 500)

| Field | Value |
|---|---|
| Affected Feature | F04 Create / F06 Edit |
| Area | Input validation |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Logged in |
| Steps to Reproduce | 1. POST task with due_date 2026-13-45 2. Open My Tasks / GET /api/tasks / Dashboard |
| Expected Result | 400; task not stored; pages still load |
| Actual Result | Task stored; every list page returns 500 permanently for that user |
| Severity | Critical |
| Priority | High |
| Evidence | TC-BB-049, TC-API-017, TC-API-018, TC-API-039; root cause characterised by TC-WB-008 (pass) |
| Status | Confirmed |

## DEF-009: Empty title accepted (web form with spaces, API PUT with "")

| Field | Value |
|---|---|
| Affected Feature | F04 Create / F06 Edit |
| Area | Input validation |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Logged in; task exists |
| Steps to Reproduce | 1. POST /tasks/new title='   ' 2. PUT /api/tasks/<id> {title:''} |
| Expected Result | 400 / form error; title kept |
| Actual Result | Blank task created; title set to '' |
| Severity | Moderate |
| Priority | Medium |
| Evidence | TC-BB-023, TC-BB-048, TC-API-035 |
| Status | Confirmed |

## DEF-010: PUT with done: "false" (string) marks the task as done

| Field | Value |
|---|---|
| Affected Feature | F07 Complete |
| Area | Input validation |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Open task |
| Steps to Reproduce | 1. PUT /api/tasks/<id> {done:'false'} |
| Expected Result | 400, or task stays open |
| Actual Result | 200; done = true |
| Severity | Moderate |
| Priority | Medium |
| Evidence | TC-API-036 |
| Status | Confirmed |

## DEF-011: Task can be created with a category id that does not exist

| Field | Value |
|---|---|
| Affected Feature | F04 Create |
| Area | Input validation |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Logged in |
| Steps to Reproduce | 1. POST /api/tasks {title:'x', category_id:999} |
| Expected Result | 400 |
| Actual Result | 201; category None |
| Severity | Minor |
| Priority | Low |
| Evidence | TC-API-019 |
| Status | Confirmed |

## DEF-012: Invalid pagination values accepted (page=-1, per_page=0); page numbering (starts at 0) not documented

| Field | Value |
|---|---|
| Affected Feature | F05 List |
| Area | API |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Tasks exist |
| Steps to Reproduce | 1. GET /api/tasks?page=-1 2. GET /api/tasks?per_page=0 |
| Expected Result | 400 |
| Actual Result | 200 with tasks / 200 [] |
| Severity | Minor |
| Priority | Low |
| Evidence | TC-API-027, TC-API-028 |
| Status | Confirmed |

## DEF-013: No maximum length for task title (5,000 characters accepted)

| Field | Value |
|---|---|
| Affected Feature | F04 Create |
| Area | Input validation |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Logged in |
| Steps to Reproduce | 1. POST /api/tasks with 5,000-char title |
| Expected Result | 400 with documented limit |
| Actual Result | 201 |
| Severity | Minor |
| Priority | Low |
| Evidence | TC-API-021 |
| Status | Confirmed |

## DEF-014: Secret key is hard-coded and the app runs in debug mode (session forgery, debugger exposed)

| Field | Value |
|---|---|
| Affected Feature | F03 Access control |
| Area | Security |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Source code available (app.py) |
| Steps to Reproduce | 1. Sign a session cookie for user_id=2 with the SECRET_KEY in app.py 2. GET /api/tasks 3. Trigger any 500 in browser |
| Expected Result | Forged cookie rejected; generic error page |
| Actual Result | qa_user2's tasks returned; Werkzeug Debugger shown |
| Severity | Critical |
| Priority | High |
| Evidence | TC-SEC-003, TC-SEC-013 |
| Status | Confirmed |

## DEF-015: No CSRF protection on state-changing forms

| Field | Value |
|---|---|
| Affected Feature | F08 Delete / F07 Toggle |
| Area | Security |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Victim logged in |
| Steps to Reproduce | 1. From another origin, POST /tasks/<id>/delete without token |
| Expected Result | 403 |
| Actual Result | Task deleted |
| Severity | Major |
| Priority | Medium |
| Evidence | TC-SEC-006 |
| Status | Confirmed |

## DEF-016: /api/categories works without logging in

| Field | Value |
|---|---|
| Affected Feature | F12 Categories |
| Area | API |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Logged out |
| Steps to Reproduce | 1. GET /api/categories |
| Expected Result | 401 |
| Actual Result | 200 with list |
| Severity | Minor |
| Priority | Low |
| Evidence | TC-API-011 |
| Status | Confirmed |

## DEF-017: Non-JSON request body gets a misleading error

| Field | Value |
|---|---|
| Affected Feature | F04 Create |
| Area | API |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Logged in |
| Steps to Reproduce | 1. POST /api/tasks text/plain 'hello' |
| Expected Result | 400/415 'body must be JSON' |
| Actual Result | 400 'title is required' |
| Severity | Minor |
| Priority | Low |
| Evidence | TC-API-020 |
| Status | Confirmed |

## DEF-018: Wrong JSON data types crash the server (HTTP 500)

| Field | Value |
|---|---|
| Affected Feature | F01 Register / F04 Create |
| Area | Input validation |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | - |
| Steps to Reproduce | 1. POST /api/register {username:12345} 2. POST /api/tasks {title:123} |
| Expected Result | 400 |
| Actual Result | 500 |
| Severity | Moderate |
| Priority | Medium |
| Evidence | TC-API-006, TC-API-016 |
| Status | Confirmed |

## DEF-019: No limit on failed login attempts (brute force possible)

| Field | Value |
|---|---|
| Affected Feature | F02 Login |
| Area | Security |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | qa_user1 exists |
| Steps to Reproduce | 1. POST wrong password 20 times |
| Expected Result | Lockout / 429 |
| Actual Result | All accepted for checking |
| Severity | Moderate |
| Priority | Medium |
| Evidence | TC-SEC-004 |
| Status | Confirmed |

## DEF-020: Session cookie still works after logout

| Field | Value |
|---|---|
| Affected Feature | F02 Logout |
| Area | Security |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Logged in |
| Steps to Reproduce | 1. Copy cookie 2. Log out 3. Replay cookie |
| Expected Result | 401 |
| Actual Result | 200 |
| Severity | Moderate |
| Priority | Medium |
| Evidence | TC-SEC-005 |
| Status | Confirmed |

## DEF-021: Form fields, filter dropdowns and the complete button have no accessible name

| Field | Value |
|---|---|
| Affected Feature | NF4 Accessibility |
| Area | GUI / accessibility |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | - |
| Steps to Reproduce | 1. Run axe on Login, Register, New Task, My Tasks |
| Expected Result | No critical violations |
| Actual Result | 'label', 'select-name' critical; button named 'white circle' |
| Severity | Major |
| Priority | Medium |
| Evidence | TC-ACC-003, TC-ACC-004, TC-ACC-011 |
| Status | Confirmed |

## DEF-022: Low colour contrast for grey text (#999 on white = 2.8:1)

| Field | Value |
|---|---|
| Affected Feature | NF4 Accessibility |
| Area | GUI / accessibility |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | - |
| Steps to Reproduce | 1. Measure contrast of empty-state and done-task text |
| Expected Result | >= 4.5:1 |
| Actual Result | 2.8:1 |
| Severity | Minor |
| Priority | Low |
| Evidence | TC-ACC-005 |
| Status | Confirmed |

## DEF-023: Layout breaks on phone width: sideways scrolling, Urgency column hidden

| Field | Value |
|---|---|
| Affected Feature | NF5 / NF4 |
| Area | GUI / accessibility |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Viewport 375x812 |
| Steps to Reproduce | 1. Open My Tasks, New Task, Dashboard |
| Expected Result | No horizontal scroll; readable text |
| Actual Result | Chrome 375 px window and Firefox 161: sideways scroll, columns cut off. Chrome 158 and Edge 158 phone emulation: desktop page shrunk to unreadable text (no viewport meta tag) |
| Severity | Moderate |
| Priority | Medium |
| Evidence | TC-GUI-014, TC-ACC-010; index_phone.png in week 3 evidence/chrome, edge, firefox |
| Status | Confirmed |

## DEF-024: No confirmation message after create, edit or delete

| Field | Value |
|---|---|
| Affected Feature | NF3 GUI |
| Area | GUI / accessibility |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | Logged in |
| Steps to Reproduce | 1. Create/edit/delete a task |
| Expected Result | Success message |
| Actual Result | Silent reload |
| Severity | Minor |
| Priority | Low |
| Evidence | TC-GUI-011 |
| Status | Confirmed |

## DEF-025: Register form clears both fields after a validation error

| Field | Value |
|---|---|
| Affected Feature | NF3 GUI |
| Area | GUI / accessibility |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | - |
| Steps to Reproduce | 1. Register with short password |
| Expected Result | Username kept |
| Actual Result | Both fields emptied |
| Severity | Minor |
| Priority | Low |
| Evidence | TC-GUI-015 |
| Status | Confirmed |

## DEF-026: Login slows above 1 s when 25+ users log in at the same moment

| Field | Value |
|---|---|
| Affected Feature | NF2 Performance |
| Area | Performance |
| Environment | Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB |
| Preconditions | perf_user; Locust |
| Steps to Reproduce | 1. Run locust -u 25 -r 25 |
| Expected Result | p95 < 1,000 ms |
| Actual Result | p95 1,200 ms (25), 2,500 ms (50) |
| Severity | Minor |
| Priority | Low |
| Evidence | TC-PERF-003, TC-PERF-004 |
| Status | Confirmed |
