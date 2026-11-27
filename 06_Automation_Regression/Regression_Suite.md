# Focused Regression Suite

Run: `pytest -m regression` (add `and not ui` without a browser).

Selection rules: high-risk areas, frequently used features, critical business rules and **every failed boundary**. Failing tests are known defects; after a fix they act as confirmation tests, and the passing ones check that the fix broke nothing.

Size: 52 tests - 28 pass, 24 fail.

| Test | Feature | Objective | Status | Defect |
|---|---|---|---|---|
| TC-BB-002 | F01 | Username of 3 chars (min) accepted | Pass |  |
| TC-BB-005 | F01 | Username of 20 chars (max) accepted | Pass |  |
| TC-BB-009 | F01 | Password of 7 chars rejected | Pass |  |
| TC-BB-010 | F01 | Password of exactly 8 chars accepted | Fail | DEF-002 |
| TC-BB-013 | F01 | Valid, new username + valid password creates account | Pass |  |
| TC-BB-014 | F01 | Taken username is refused | Fail | DEF-004 |
| TC-BB-017 | F02 | Existing user + correct password logs in | Pass |  |
| TC-BB-021 | F04 | Task with title, category and valid due date created | Pass |  |
| TC-BB-023 | F04 | Title of spaces only is refused (server) | Fail | DEF-009 |
| TC-BB-024 | F04 | Special characters shown as text | Fail | DEF-007 |
| TC-BB-025 | F10 | Yesterday -> Overdue | Pass |  |
| TC-BB-026 | F10 | Today -> Due Today | Fail | DEF-001 |
| TC-BB-027 | F10 | Tomorrow -> Due Soon | Pass |  |
| TC-BB-029 | F10 | Day 3 -> Upcoming | Pass |  |
| TC-BB-032 | F07 | Toggle open task completes it and sets completed_at | Pass |  |
| TC-BB-033 | F07 | Toggle done task reopens it and clears completed_at | Pass |  |
| TC-BB-034 | F08 | Owner deletes task | Pass |  |
| TC-BB-037 | F03 | Logged-out user opening a protected page is redirected | Pass |  |
| TC-BB-039 | F09 | Category filter shows only that category | Pass |  |
| TC-BB-045 | F11 | Dashboard counters match seeded data | Pass |  |
| TC-BB-046 | F11 | Task due today is not counted as Overdue | Fail | DEF-001 |
| TC-BB-049 | F04 | Impossible date is refused | Fail | DEF-008 |
| TC-WB-001 | F10 | No due date | Pass |  |
| TC-WB-003 | F10 | Past date | Pass |  |
| TC-WB-004 | F10 | Due today | Fail | DEF-001 |
| TC-WB-005 | F10 | 1 day away | Pass |  |
| TC-WB-007 | F10 | 3 days away | Pass |  |
| TC-WB-010 | F01 | is_valid_password 8 chars | Fail | DEF-002 |
| TC-WB-021 | F11 | Completed exactly 7 days ago | Fail | DEF-003 |
| TC-API-001 | F01 | Register valid user | Pass |  |
| TC-API-005 | F01 | Duplicate username rejected | Fail | DEF-004 |
| TC-API-007 | F02 | Login valid | Pass |  |
| TC-API-013 | F04 | Create task with all fields | Pass |  |
| TC-API-017 | F04 | Impossible date rejected | Fail | DEF-008 |
| TC-API-024 | F03 | Other user's task hidden | Pass |  |
| TC-API-033 | F09 | Search with an apostrophe works like the web UI | Fail | DEF-006 |
| TC-API-035 | F06 | PUT empty title rejected | Fail | DEF-009 |
| TC-API-036 | F07 | done='false' (string) not treated as true | Fail | DEF-010 |
| TC-API-040 | F08 | Delete own task | Pass |  |
| TC-API-042 | F03 | Cannot delete another user's task | Fail | DEF-005 |
| TC-API-043 | F08 | Delete needs login | Pass |  |
| TC-API-045 | F11 | Task due today not counted as overdue | Fail | DEF-001 |
| TC-SEC-003 | F03 | Cookie cannot be forged from source code | Fail | DEF-014 |
| TC-SEC-006 | F08 | State-changing form needs a CSRF token | Fail | DEF-015 |
| TC-SEC-008 | F03 | DELETE other user's task refused | Fail | DEF-005 |
| TC-SEC-009 | F03 | GET other user's task refused | Pass |  |
| TC-SEC-010 | F09 | Search input cannot change the SQL query | Fail | DEF-006 |
| TC-SEC-012 | F05 | Script in title is escaped | Fail | DEF-007 |
| AT-001 | F01 | Register and land on My Tasks | Pass |  |
| AT-002 | F01 | 8-character password accepted | Fail | DEF-002 |
| AT-003 | F02 | Login, logout, protected page | Pass |  |
| AT-004 | F10 | Due-today badge | Fail | DEF-001 |
