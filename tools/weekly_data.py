"""Structured data for the weekly Data Collection workbooks (same content as the
markdown documents in each week folder). Edit here, then run tools/build_documents.py."""

SCOPE = [  # ID, feature, business rule, users/entry point, likelihood, impact, techniques, in scope
    ("F01", "Registration", "Username 3–20 chars (letters, digits, _); password ≥ 8 chars", "Web form + API", 2, 2, "EP, BVA, decision table, API, unit", "Yes"),
    ("F02", "Login / logout", "Correct credentials start a session; logout ends it", "Web form + API", 2, 2, "Decision table, state transition, security", "Yes"),
    ("F03", "Access control", "Logged out → redirect / 401; users reach only their own tasks", "All pages + API", 2, 3, "State transition, API negative, STRIDE", "Yes"),
    ("F04", "Create task", "Title required; category and due date (YYYY-MM-DD) optional", "Web form + API", 2, 3, "EP, API negative, XSS", "Yes"),
    ("F05", "View / list", "Newest first; API pagination (page, per_page)", "My Tasks + API", 1, 1, "API, pagination edges", "Yes"),
    ("F06", "Edit task", "Edit fields; API partial update", "Edit page + API PUT", 2, 3, "EP, state transition, API", "Yes"),
    ("F07", "Complete / reopen", "completed_at set when done, cleared when reopened", "Toggle button + API PUT", 1, 2, "State transition, branch", "Yes"),
    ("F08", "Delete task", "Only the owner can delete", "Delete button + API DELETE", 2, 3, "State transition, API, CSRF", "Yes"),
    ("F09", "Filter / search", "Category and status filters; search on part of the title", "My Tasks + API", 2, 3, "EP, SQL injection", "Yes"),
    ("F10", "Urgency", "No due date / Overdue / Due Today / Due Soon (1–2) / Upcoming (3+) / Done", "Badge on My Tasks", 2, 2, "BVA (−1,0,1,2,3), basis path", "Yes"),
    ("F11", "Dashboard", "Total, Open, Overdue, Due Soon, Completed in last 7 days (inclusive)", "Dashboard + API", 2, 2, "EP, BVA, branch", "Yes"),
    ("F12", "Categories", "Work, Personal, Study, Urgent", "Dropdowns + API", 1, 1, "API", "Yes"),
    ("NF2", "Performance", "Responsive at expected load", "API", 1, 2, "Locust load/stress", "Yes"),
    ("NF3", "GUI / usability", "Clear, consistent, gives feedback", "All pages", 2, 2, "Checklist, LEMES", "Yes"),
    ("NF4", "Accessibility", "WCAG 2.1 AA", "All pages", 1, 2, "axe-core + manual", "Yes"),
    ("NF5", "Compatibility", "Chrome, Edge and Firefox at desktop, tablet and phone size", "All pages", 2, 1, "Browser × viewport", "Yes (Safari out of scope)"),
]

UNITS = [  # unit, why, V(G), tests
    ("helpers.compute_urgency", "Most important business rule; 4 decisions; drives badges and dashboard", 5, "TC-WB-001–008"),
    ("helpers.is_valid_password", "Registration gate; boundary at 8 (one decision)", 2, "TC-WB-009–012"),
    ("helpers.is_valid_username", "Registration gate; range and character rules", 4, "TC-WB-013–018"),
    ("helpers.completed_in_last_n_days", "Dashboard counter; inclusive boundary; compound condition", 4, "TC-WB-019–025"),
    ("app.api_update_task (completed_at)", "if / elif that sets or clears completion time", 3, "TC-WB-026–029"),
]

USABILITY = [  # dimension, positive, issue, defect
    ("Learnability", "Simple layout; first task created in under a minute", "Hint says 8 characters but 9 are enforced", "DEF-002"),
    ("Efficiency", "Dropdown filters apply instantly", "Search needs the Filter button (inconsistent); no sort by due date", "–"),
    ("Memorability", "Same top bar and styles on every page", "–", "–"),
    ("Errors", "Delete confirmation; plain-language error messages", "No success messages; register form clears input; one bad date crashes the list", "DEF-024, DEF-025, DEF-008"),
    ("Satisfaction", "Clean look; badges use text and colour", "Phone layout needs sideways scrolling", "DEF-023"),
]

COMPAT = [  # browser/OS, desktop, tablet, phone, test, status
    ("Chrome 153 / Linux", "Pass", "Pass", "Fail (DEF-023)", "TC-COMP-001, TC-GUI-012–014", "Executed – cloud verification run"),
    ("Chrome 158 / Windows 11", "Pass", "Pass", "Fail (DEF-023)", "TC-COMP-002", "Executed – member laptop, 27 Nov 2026"),
    ("Edge 158 / Windows 11", "Pass", "Pass", "Fail (DEF-023)", "TC-COMP-003", "Executed – member laptop, 27 Nov 2026"),
    ("Firefox 161 / Windows 11", "Pass", "Pass", "Fail (DEF-023)", "TC-COMP-004", "Executed – member laptop, 27 Nov 2026"),
]

WEB_SCENARIOS = [  # id, scenario, steps, covered by, result
    ("WS-01", "New user onboarding", "Register → land on My Tasks → empty state", "TC-BB-002, AT-001", "Pass"),
    ("WS-02", "Daily task management", "Log in → create → complete → reopen → edit → delete", "TC-BB-021, 032–034, 047, AT-005, AT-006", "Pass"),
    ("WS-03", "Finding tasks", "Filter by category / status → search → combined", "TC-BB-039–044, AT-007", "Pass"),
    ("WS-04", "Deadline overview", "Tasks due −1/0/1/2/3 days → badges → dashboard", "TC-BB-025–031, 045–046, AT-004, AT-009", "Fail (DEF-001)"),
    ("WS-05", "Session security", "Log out → protected page → redirect", "TC-BB-037–038, AT-003", "Pass"),
    ("WS-06", "Client vs server validation", "Same bad input via browser and via direct request", "see UI vs API sheet", "Fail (DEF-004–009)"),
]

UI_VS_API = [  # input, browser, server/API, defect
    ("Empty title", "Blocked by 'required'", "Saved by form post and API PUT", "DEF-009"),
    ("Impossible date", "Date picker prevents it", "Saved, then HTTP 500 on every list", "DEF-008"),
    ("Apostrophe in search", "Web search works (parameterised)", "API search returns HTTP 500 (f-string SQL)", "DEF-006"),
    ("Delete another user's task", "Not possible (scoped by user_id)", "Possible (DELETE not scoped)", "DEF-005"),
    ("Duplicate username", "Accepted", "Accepted", "DEF-004"),
]

STRIDE = [  # asset, category, threat, property, tests, result
    ("Login / session cookie", "Spoofing", "Forge a session cookie with the secret in the source code", "Authenticity", "TC-SEC-002, 003", "Forgery works (DEF-014)"),
    ("Login", "Spoofing", "Password guessing with unlimited attempts", "Authenticity", "TC-SEC-004", "No limit (DEF-019)"),
    ("Logout", "Spoofing", "Stolen cookie replayed after logout", "Authenticity", "TC-SEC-005", "Still valid (DEF-020)"),
    ("Task API (PUT/DELETE)", "Tampering", "Change or delete another user's task", "Integrity", "TC-SEC-007, 008", "PUT safe; DELETE unsafe (DEF-005)"),
    ("Web forms", "Tampering", "Cross-site request forges delete / toggle", "Integrity", "TC-SEC-006", "Accepted (DEF-015)"),
    ("Task list page", "Tampering", "Stored script in a title runs in the browser (XSS)", "Integrity", "TC-SEC-012", "Rendered (DEF-007)"),
    ("All actions", "Repudiation", "User denies a change; no audit trail", "Non-repudiation", "Code review", "No audit log (observation)"),
    ("Task search", "Information disclosure", "SQL injection returns other users' tasks", "Confidentiality", "TC-SEC-010", "Leaks data (DEF-006)"),
    ("Task API (GET)", "Information disclosure", "Read another user's task by id", "Confidentiality", "TC-SEC-009, TC-API-024", "Protected (404)"),
    ("Error pages", "Information disclosure", "Debugger shows code and paths", "Confidentiality", "TC-SEC-013", "Exposed (DEF-014)"),
    ("User table", "Information disclosure", "Passwords readable if DB copied", "Confidentiality", "TC-SEC-011", "Hashed (scrypt)"),
    ("Task list / dashboard", "Denial of service", "One invalid date crashes the user's pages", "Availability", "TC-API-017, TC-BB-049", "Crashes (DEF-008)"),
    ("Login", "Denial of service", "Burst of logins slows the server", "Availability", "TC-PERF-003/004", "Slow > 1 s (DEF-026)"),
    ("Edit page / API", "Elevation of privilege", "Normal user acts on another user's resources", "Authorization", "TC-SEC-014, 008", "Edit page safe; API delete unsafe (DEF-005)"),
]

PERF_PLAN = [
    ("Objective", "Response time (avg, p95), throughput and error rate as users increase; defined before execution"),
    ("Criterion", "p95 < 1,000 ms and 0% errors for every request type"),
    ("Tool", "Locust (05_Security_Performance/performance/locustfile.py)"),
    ("Workload", "Log in once as perf_user (100 tasks), then 60% GET /api/tasks, 30% GET /api/dashboard, 10% POST /api/tasks; think time 1–2 s"),
    ("Load levels", "1, 10, 25, 50 users (all start at once), 40 s each"),
    ("Stress step", "100 users added at 10/s, 40 s"),
    ("Environment", "Flask development server (debug on), SQLite, load generator on the same 2-vCPU / 8 GB machine"),
]

PERF_RESULTS = [  # users, task avg/p95, dash avg/p95, login avg/p95, req/s, errors, result
    (1, "4.4 / 5", "5.0 / 6", "117.3 / 120", 0.72, 0, "Pass"),
    (10, "4.2 / 6", "6.0 / 11", "567.3 / 610", 6.87, 0, "Pass"),
    (25, "5.4 / 9", "6.9 / 10", "1105.9 / 1200", 17.06, 0, "Fail (DEF-026)"),
    (50, "7.0 / 9", "10.1 / 12", "2105.8 / 2500", 33.15, 0, "Fail (DEF-026)"),
    ("100 (stress)", "5.9 / 16", "12.2 / 45", "482.9 / 560", 61.36, 0, "Pass"),
]

LIMITS = [  # area, limitation, recommendation
    ("Performance", "Dev server, shared CPU with load generator, SQLite, 40 s runs, no CPU/memory monitoring – trends only", "Repeat on a production WSGI server with debug off, ≥ 10 min per level, with monitoring"),
    ("Performance", "Login bottleneck in bursts (scrypt hashing)", "Add login rate limiting; consider async hashing / worker pool"),
    ("Security", "No automated scanner (brief forbids uncontrolled testing)", "OWASP ZAP baseline scan in a controlled environment"),
    ("Security", "Hard-coded secret + debug mode", "SECRET_KEY from environment; debug off; Bandit in CI"),
    ("Security", "Cross-user delete, SQL injection, XSS, CSRF", "Scope queries by user_id; parameterised SQL; remove |safe; Flask-WTF CSRF"),
    ("Security", "No audit log (repudiation)", "Log create / edit / delete with user and time"),
]

CANDIDATES = [  # group, repetition, stable, critical, regression value, decision
    ("BVA / EP on registration and urgency", "High", "Yes", "Yes", "Every failed boundary", "Automate (PyTest)"),
    ("helpers.py rules", "High", "Yes", "Yes", "Yes", "Automate (unit)"),
    ("API happy and negative paths", "High", "Yes", "Yes", "Yes", "Automate (Flask client)"),
    ("Cross-user / injection / XSS checks", "Medium", "Yes", "Critical", "Yes", "Automate (security)"),
    ("Main UI journeys", "Medium", "Mostly", "Yes", "Yes", "Automate 10 (Selenium, POM)"),
    ("Look and feel, usability judgement", "Low", "No", "–", "–", "Manual"),
    ("WCAG judgement (contrast, screen reader)", "Low", "–", "–", "–", "Manual + axe"),
    ("One-off browser checks", "Low", "–", "–", "–", "Manual smoke"),
    ("Debugger exposure (TC-SEC-013)", "Once", "–", "–", "–", "Manual"),
]

REFLECTION = [  # area, observation, evidence, recommendation
    ("Speed", "137 non-UI tests run in about 20 s, so they were re-run many times with identical results", "07_Test_Management/Execution_Evidence/pytest_all.log", "Run on every commit (CI)"),
    ("Consistency", "Generating spreadsheets, RTM and metrics from one catalogue kept IDs and statuses consistent", "tools/build_documents.py", "Keep a single source of truth"),
    ("Confirmation tests", "24 failing regression tests become confirmation tests once defects are fixed", "Regression_Suite.md", "Re-run pytest -m regression after each fix"),
    ("Cost", "Scripts took longer to write than one manual run", "–", "Automate only stable, repeated, critical tests"),
    ("Flakiness", "One Selenium test was flaky until explicit waits were added", "pages/base_page.py", "Use explicit waits, never sleep"),
    ("Limits", "Automation cannot judge usability; 100% coverage did not mean correct code", "TC-WB-004, 010, 021", "Keep manual exploratory and usability review"),
]
