"""
PyTodo Pro QA - single source of truth for every test case and defect.

Every spreadsheet, the RTM, the defect log and the metrics in this repository
are generated from this file (see tools/build_documents.py).  If you change a
test case or a result, change it HERE and re-run `bash tools/run_all.sh`.

Field order follows the Test Case Template in the Group Project 2 brief:
ID, Feature/Requirement, Technique/Test Type, Objective, Preconditions,
Test Data, Steps, Expected Result, Actual Result, Status, Evidence, Defect ID.
Extra management fields: Priority, Automated (script), Regression flag.
"""

from collections import OrderedDict

PASS, FAIL, NOT_RUN, BLOCKED = "Pass", "Fail", "Not Run", "Blocked"

FEATURES = OrderedDict([
    ("F01", "Registration"),
    ("F02", "Login / logout"),
    ("F03", "Access control"),
    ("F04", "Create task"),
    ("F05", "View / list"),
    ("F06", "Edit task"),
    ("F07", "Complete / reopen"),
    ("F08", "Delete task"),
    ("F09", "Filter / search"),
    ("F10", "Urgency"),
    ("F11", "Dashboard"),
    ("F12", "Categories"),
    ("NF2", "Performance"),
    ("NF3", "GUI / usability"),
    ("NF4", "Accessibility"),
    ("NF5", "Compatibility"),
])

PHASES = OrderedDict([
    ("BB", ("Black-box (Wk 1)", "01_Black_Box/test_black_box.py")),
    ("WB", ("White-box (Wk 2)", "02_White_Box_Coverage/test_helpers_unit.py")),
    ("GUI", ("GUI & config (Wk 3)", "03_Special_Testing (manual checklist)")),
    ("ACC", ("Accessibility (Wk 3)", "03_Special_Testing (Axe + manual)")),
    ("COMP", ("Compatibility (Wk 3)", "03_Special_Testing (manual)")),
    ("API", ("Web & API (Wk 4)", "04_Web_API/test_api.py")),
    ("SEC", ("Security (Wk 5)", "05_Security_Performance/test_security.py")),
    ("PERF", ("Performance (Wk 5)", "05_Security_Performance/performance/locustfile.py")),
    ("AT", ("UI automation (Wk 6)", "06_Automation_Regression/test_ui_selenium.py")),
])

TEST_CASES = []


def tc(id_, feature, technique, objective, pre, data, steps, expected, actual,
       status, defect="", priority="Medium", automated=True, regression=False,
       evidence=None):
    phase = id_.split("-")[1] if id_.startswith("TC-") else "AT"
    if evidence is None:
        if automated:
            script = PHASES[phase][1]
            fn = "test_" + id_.lower().replace("-", "_")
            evidence = f"{script}::{fn}; junit log in reports/"
        else:
            evidence = PHASES[phase][1]
    TEST_CASES.append(OrderedDict([
        ("Test Case ID", id_),
        ("Feature/Requirement", feature),
        ("Technique/Test Type", technique),
        ("Objective", objective),
        ("Preconditions", pre),
        ("Test Data", data),
        ("Steps", steps),
        ("Expected Result", expected),
        ("Actual Result", actual),
        ("Status", status),
        ("Evidence", evidence),
        ("Defect ID", defect),
        ("Priority", priority),
        ("Automated", "Yes" if automated else "No"),
        ("Regression", "Yes" if regression else "No"),
        ("Phase", PHASES[phase][0]),
    ]))


# ---------------------------------------------------------------------------
# Week 1 - Black-box (49): EP, BVA (3-value), decision table, state transition
# ---------------------------------------------------------------------------
REG = "1. Open /register 2. Enter username and password 3. Click Register"
H, M, L = "High", "Medium", "Low"

tc("TC-BB-001", "F01", "BVA (3-value)", "Username of 2 chars (below min) rejected", "Logged out; fresh DB",
   "username='ab', password='Passw0rd!'", REG, "Error 'Username must be 3-20 characters...'; no account",
   "Error shown; no account created", PASS, priority=H)
tc("TC-BB-002", "F01", "BVA (3-value)", "Username of 3 chars (min) accepted", "Logged out; fresh DB",
   "username='abc', password='Passw0rd!'", REG, "Account created; redirected to My Tasks (/)",
   "Account created; redirected to /", PASS, priority=H, regression=True)
tc("TC-BB-003", "F01", "BVA (3-value)", "Username of 4 chars accepted", "Logged out; fresh DB",
   "username='abcd'", REG, "Account created", "Account created", PASS, priority=L)
tc("TC-BB-004", "F01", "BVA (3-value)", "Username of 19 chars accepted", "Logged out; fresh DB",
   "username='u'*19", REG, "Account created", "Account created", PASS, priority=L)
tc("TC-BB-005", "F01", "BVA (3-value)", "Username of 20 chars (max) accepted", "Logged out; fresh DB",
   "username='u'*20", REG, "Account created", "Account created", PASS, priority=H, regression=True)
tc("TC-BB-006", "F01", "BVA (3-value)", "Username of 21 chars (above max) rejected", "Logged out; fresh DB",
   "username='u'*21", REG, "Username error; no account", "Error shown; no account", PASS, priority=H)
tc("TC-BB-007", "F01", "EP (invalid: space)", "Username containing a space rejected", "Logged out",
   "username='qa user'", REG, "Username error; no account", "Error shown; no account", PASS, priority=M)
tc("TC-BB-008", "F01", "EP (invalid: symbol)", "Username containing a symbol rejected", "Logged out",
   "username='qa-user!'", REG, "Username error; no account", "Error shown; no account", PASS, priority=M)
tc("TC-BB-009", "F01", "BVA (3-value)", "Password of 7 chars rejected", "Logged out",
   "password='Abc123!'", REG, "Error 'Password must be at least 8 characters.'", "Error shown", PASS,
   priority=H, regression=True)
tc("TC-BB-010", "F01", "BVA (3-value)", "Password of exactly 8 chars accepted", "Logged out",
   "password='Abcd123!'", REG, "Account created; redirected to /",
   "8-character password refused with 'Password must be at least 8 characters.'", FAIL, "DEF-002",
   priority=H, regression=True)
tc("TC-BB-011", "F01", "BVA (3-value)", "Password of 9 chars accepted", "Logged out",
   "password='Abcd1234!'", REG, "Account created", "Account created", PASS, priority=H)
tc("TC-BB-012", "F01", "EP (invalid: empty)", "Empty password rejected (server)", "Logged out",
   "password=''", "POST /register with empty password", "Password error; no account", "Error shown", PASS,
   priority=M)
tc("TC-BB-013", "F01", "Decision table R1 (Y,Y,Y)", "Valid, new username + valid password creates account",
   "Logged out", "username='dt_new', password='Passw0rd!'", REG, "Account created",
   "Account created", PASS, priority=H, regression=True)
tc("TC-BB-014", "F01", "Decision table R2 (Y,Y,N)", "Taken username is refused",
   "'dt_taken' already registered", "username='dt_taken'", REG + " (second time)",
   "Registration refused with 'username already taken'",
   "Duplicate username 'dt_taken' registered again (HTTP 302 to /)", FAIL, "DEF-004", priority=H,
   regression=True)
tc("TC-BB-015", "F01", "Decision table R3 (Y,N,-)", "Valid username + invalid password -> password error",
   "Logged out", "username='dt_pw', password='short'", REG, "Password error", "Password error", PASS,
   priority=H)
tc("TC-BB-016", "F01", "Decision table R4 (N,-,-)", "Invalid username -> username error", "Logged out",
   "username='x', password='Passw0rd!'", REG, "Username error", "Username error", PASS, priority=H)
LOGIN = "1. Open /login 2. Enter credentials 3. Click Log in"
tc("TC-BB-017", "F02", "Decision table (login R1)", "Existing user + correct password logs in",
   "qa_user1 registered", "qa_user1 / Passw0rd!", LOGIN, "Session started; redirected to /",
   "Logged in; redirected to /", PASS, priority=H, regression=True)
tc("TC-BB-018", "F02", "Decision table (login R2)", "Existing user + wrong password refused",
   "qa_user1 registered", "qa_user1 / WrongPass1", LOGIN, "'Invalid username or password.'",
   "Message shown", PASS, priority=H)
tc("TC-BB-019", "F02", "Decision table (login R3)", "Unknown user refused", "-", "ghost / Passw0rd!",
   LOGIN, "'Invalid username or password.'", "Message shown", PASS, priority=M)
tc("TC-BB-020", "F02", "Decision table (derived from R2)", "Second account with same name can log in (or is refused)",
   "'dup_user' registered twice with different passwords", "dup_user / second password",
   "1. Register dup_user twice 2. Log in with second password",
   "Second registration refused, or second account can log in",
   "Second 'dup_user' account created but cannot log in ('Invalid username or password.')", FAIL,
   "DEF-004", priority=H)
NEW = "1. Log in 2. Open New Task 3. Fill fields 4. Save"
tc("TC-BB-021", "F04", "EP (valid)", "Task with title, category and valid due date created", "Logged in as qa_user1",
   "title='Write report', category=Work, due=today+3", NEW, "Task listed with category and 'Upcoming'",
   "Task listed correctly", PASS, priority=H, regression=True)
tc("TC-BB-022", "F04", "EP (valid: optional fields empty)", "Task with title only created", "Logged in",
   "title='Read book'", NEW, "Task listed; 'No due date'", "Task listed; 'No due date'", PASS, priority=M)
tc("TC-BB-023", "F04", "EP (invalid: whitespace title)", "Title of spaces only is refused (server)", "Logged in",
   "title='   ' (posted directly, bypassing 'required')", "POST /tasks/new with title of spaces",
   "Task not created; error asks for a title", "Task with an empty title was created (blank row in My Tasks)",
   FAIL, "DEF-009", priority=H, regression=True)
tc("TC-BB-024", "F04", "EP (valid: special characters)", "Special characters shown as text", "Logged in",
   "title='Buy milk & eggs <urgent>'", NEW, "List shows the full text 'Buy milk & eggs <urgent>'",
   "Title inserted as raw HTML; '<urgent>' becomes an HTML tag and is not shown", FAIL, "DEF-007",
   priority=H, regression=True)
URG = "1. Create task with due date 2. Open My Tasks 3. Read Urgency badge"
tc("TC-BB-025", "F10", "BVA (day -1)", "Yesterday -> Overdue", "Logged in", "due=today-1", URG,
   "Badge 'Overdue'", "Badge 'Overdue'", PASS, priority=H, regression=True)
tc("TC-BB-026", "F10", "BVA (day 0)", "Today -> Due Today", "Logged in", "due=today", URG,
   "Badge 'Due Today'", "Badge 'Overdue'", FAIL, "DEF-001", priority=H, regression=True)
tc("TC-BB-027", "F10", "BVA (day 1)", "Tomorrow -> Due Soon", "Logged in", "due=today+1", URG,
   "Badge 'Due Soon'", "Badge 'Due Soon'", PASS, priority=H, regression=True)
tc("TC-BB-028", "F10", "BVA (day 2)", "Day 2 -> Due Soon", "Logged in", "due=today+2", URG,
   "Badge 'Due Soon'", "Badge 'Due Soon'", PASS, priority=H)
tc("TC-BB-029", "F10", "BVA (day 3)", "Day 3 -> Upcoming", "Logged in", "due=today+3", URG,
   "Badge 'Upcoming'", "Badge 'Upcoming'", PASS, priority=H, regression=True)
tc("TC-BB-030", "F10", "EP (no due date)", "No due date -> 'No due date'", "Logged in", "due empty", URG,
   "Badge 'No due date'", "Badge 'No due date'", PASS, priority=M)
tc("TC-BB-031", "F10", "EP (completed)", "Completed task -> 'Done'", "Logged in; task completed", "due=today-1",
   "1. Complete task 2. Read badge", "Badge 'Done' (not Overdue)", "Badge 'Done'", PASS, priority=M)
tc("TC-BB-032", "F07", "State transition Open->Done", "Toggle open task completes it and sets completed_at",
   "Open task exists", "-", "1. Click complete (o) on task", "Task shown as done; completed_at set",
   "As expected", PASS, priority=H, regression=True)
tc("TC-BB-033", "F07", "State transition Done->Open", "Toggle done task reopens it and clears completed_at",
   "Done task exists", "-", "1. Click (check) on done task", "Task open; completed_at cleared",
   "As expected", PASS, priority=H, regression=True)
tc("TC-BB-034", "F08", "State transition Open->Deleted", "Owner deletes task", "Open task exists", "-",
   "1. Click Delete 2. Confirm", "Task removed from list", "Task removed", PASS, priority=H, regression=True)
tc("TC-BB-035", "F07", "State transition Deleted->toggle (invalid)", "Toggling a deleted task is refused safely",
   "Task deleted", "deleted task id", "POST /tasks/<id>/toggle", "404 or redirect; nothing changes",
   "Refused safely: redirected to My Tasks (302); nothing changed", PASS, priority=H)
tc("TC-BB-036", "F06", "State transition Deleted->edit (invalid)", "Editing a deleted task is refused safely",
   "Task deleted", "deleted task id", "GET/POST /tasks/<id>/edit", "404 or redirect", "Refused safely: redirected to My Tasks (302)",
   PASS, priority=H)
tc("TC-BB-037", "F03", "State transition (session)", "Logged-out user opening a protected page is redirected",
   "Logged out", "-", "Open / and /dashboard", "Redirect to /login", "Redirected to /login", PASS,
   priority=H, regression=True)
tc("TC-BB-038", "F02", "State transition (session)", "After logout, protected page needs login again",
   "Logged in", "-", "1. Log out 2. Open /", "Redirect to /login", "Redirected to /login", PASS, priority=H)
FIL = "1. Log in with seeded tasks 2. Apply filter/search 3. Read list"
tc("TC-BB-039", "F09", "EP (category filter)", "Category filter shows only that category", "Tasks in Work and Study",
   "category=Work", FIL, "Only Work tasks", "Only Work tasks", PASS, priority=M, regression=True)
tc("TC-BB-040", "F09", "EP (status filter)", "Status filter shows only done / only open tasks", "Open and done tasks",
   "status=done; status=open", FIL, "done: only done tasks; open: only open tasks", "As expected", PASS, priority=M)
tc("TC-BB-041", "F09", "EP (partial match)", "Search matches part of the title", "Task 'Write report'",
   "q='repo'", FIL, "'Write report' listed", "Listed", PASS, priority=M)
tc("TC-BB-042", "F09", "EP (no match)", "Search with no match shows empty state", "Tasks exist",
   "q='zzz'", FIL, "No tasks; empty-state message", "Empty state shown", PASS, priority=L)
tc("TC-BB-043", "F09", "EP (combined)", "Category + search combined", "Tasks exist", "category=Work, q='report'",
   FIL, "Only matching Work tasks", "As expected", PASS, priority=L)
tc("TC-BB-044", "F09", "EP (apostrophe)", "Search containing an apostrophe works in web UI", "Task \"Mum's birthday\"",
   "q=\"Mum's\"", FIL, "Task listed; no error", "Task listed", PASS, priority=M)
DASH = "1. Log in with seeded tasks 2. Open /dashboard 3. Read counters"
tc("TC-BB-045", "F11", "EP (counters)", "Dashboard counters match seeded data", "5 seeded tasks (see data)",
   "1 overdue, 1 due soon, 1 upcoming, 1 no date, 1 done today", DASH,
   "Total 5, Open 4, Overdue 1, Due Soon 1, Completed 1", "As expected", PASS, priority=H, regression=True)
tc("TC-BB-046", "F11", "BVA (day 0)", "Task due today is not counted as Overdue", "One open task due today",
   "due=today", DASH, "Overdue 0", "Overdue = 1", FAIL, "DEF-001", priority=H, regression=True)
tc("TC-BB-047", "F06", "State transition Open->Open (edit)", "Edit title, category and due date", "Open task",
   "new title 'Edited', category Study, due today+5", "1. Click Edit 2. Change fields 3. Save",
   "Changes saved; still open", "Changes saved", PASS, priority=H)
tc("TC-BB-048", "F06", "EP (invalid: whitespace title)", "Edit to a title of spaces is refused", "Open task",
   "title='   ' (posted directly)", "POST /tasks/<id>/edit", "Change refused; old title kept",
   "Title changed to '' (empty)", FAIL, "DEF-009", priority=H)
tc("TC-BB-049", "F04", "EP (invalid date, client check bypassed)", "Impossible date is refused", "Logged in",
   "due='2026-13-45' (posted directly)", "1. POST /tasks/new 2. Open My Tasks",
   "Task refused with a date error; My Tasks still loads",
   "Task was saved and My Tasks now returns HTTP 500 (Internal Server Error)", FAIL, "DEF-008",
   priority=H, regression=True)

# ---------------------------------------------------------------------------
# Week 2 - White-box (29) on helpers.py and app.api_update_task
# today = 2026-11-21 for every compute_urgency test
# ---------------------------------------------------------------------------
UT = "Call the function with the test data (PyTest)"
tc("TC-WB-001", "F10", "Basis path 1-3-4-10", "No due date", "today=2026-11-21", "due=None", UT,
   "'No due date'", "'No due date'", PASS, priority=H, regression=True)
tc("TC-WB-002", "F10", "Basis path 1-2-3-5-7-9-10", "today defaulted (None) branch", "-", "due=today+30, today=None",
   UT, "'Upcoming'", "'Upcoming'", PASS, priority=M)
tc("TC-WB-003", "F10", "Basis path 1-3-5-6-10", "Past date", "today=2026-11-21", "due=2026-11-20", UT,
   "'Overdue'", "'Overdue'", PASS, priority=H, regression=True)
tc("TC-WB-004", "F10", "Boundary of 'due <= today'", "Due today", "today=2026-11-21", "due=2026-11-21", UT,
   "'Due Today'", "'Overdue' (no branch can return 'Due Today')", FAIL, "DEF-001", priority=H, regression=True)
tc("TC-WB-005", "F10", "Basis path 1-3-5-7-8-10", "1 day away", "today=2026-11-21", "due=2026-11-22", UT,
   "'Due Soon'", "'Due Soon'", PASS, priority=H, regression=True)
tc("TC-WB-006", "F10", "Branch (days == 2)", "2 days away", "today=2026-11-21", "due=2026-11-23", UT,
   "'Due Soon'", "'Due Soon'", PASS, priority=H)
tc("TC-WB-007", "F10", "Basis path 1-3-5-7-9-10", "3 days away", "today=2026-11-21", "due=2026-11-24", UT,
   "'Upcoming'", "'Upcoming'", PASS, priority=H, regression=True)
tc("TC-WB-008", "F10", "Data-flow (define-store-use)", "Characterise invalid stored date", "today=2026-11-21",
   "due='2026-13-45'", UT, "Raises ValueError (documents root cause of DEF-008)", "ValueError raised", PASS,
   priority=M)
tc("TC-WB-009", "F01", "Branch (len < 8)", "is_valid_password 7 chars", "-", "'Abc123!'", UT, "False", "False",
   PASS, priority=H)
tc("TC-WB-010", "F01", "Boundary (len == 8)", "is_valid_password 8 chars", "-", "'Abcd123!'", UT, "True",
   "False (condition is len > 8)", FAIL, "DEF-002", priority=H, regression=True)
tc("TC-WB-011", "F01", "Branch (len > 8)", "is_valid_password 9 chars", "-", "'Abcd1234!'", UT, "True", "True",
   PASS, priority=M)
tc("TC-WB-012", "F01", "Branch (empty/None)", "is_valid_password empty or non-string", "-", "'' and None", UT, "False", "False", PASS,
   priority=M)
tc("TC-WB-013", "F01", "Branch (len < 3 / non-string)", "is_valid_username 2 chars or non-string", "-", "'ab' and None", UT, "False", "False", PASS,
   priority=M)
tc("TC-WB-014", "F01", "Boundary (len == 3)", "is_valid_username 3 chars", "-", "'abc'", UT, "True", "True", PASS,
   priority=H)
tc("TC-WB-015", "F01", "Boundary (len == 20)", "is_valid_username 20 chars", "-", "'u'*20", UT, "True", "True",
   PASS, priority=H)
tc("TC-WB-016", "F01", "Branch (len > 20)", "is_valid_username 21 chars", "-", "'u'*21", UT, "False", "False",
   PASS, priority=M)
tc("TC-WB-017", "F01", "Branch (bad characters)", "is_valid_username with symbol", "-", "'qa-user'", UT, "False",
   "False", PASS, priority=M)
tc("TC-WB-018", "F01", "Branch (underscore/digits)", "is_valid_username letters, digits, _", "-", "'qa_user1'", UT,
   "True", "True", PASS, priority=L)
CN = "Call completed_in_last_n_days(completed_at, n=7, now=2026-11-21 12:00)"
tc("TC-WB-019", "F11", "Branch (None)", "Not completed", "-", "completed_at=None", CN, "False", "False", PASS,
   priority=M)
tc("TC-WB-020", "F11", "Branch (inside window)", "Completed 3 days ago", "-", "2026-11-18 12:00", CN, "True",
   "True", PASS, priority=M)
tc("TC-WB-021", "F11", "Boundary (exactly 7 days, inclusive)", "Completed exactly 7 days ago", "-",
   "2026-11-14 12:00", CN, "True (window is inclusive)", "False (condition age.days < n)", FAIL, "DEF-003",
   priority=H, regression=True)
tc("TC-WB-022", "F11", "Branch (outside window)", "Completed 8 days ago", "-", "2026-11-13 12:00", CN, "False",
   "False", PASS, priority=M)
tc("TC-WB-023", "F11", "Condition (age > 0 false)", "Completed in the future (clock skew)", "-", "2026-11-22 12:00",
   CN, "False", "False", PASS, priority=L)
tc("TC-WB-024", "F11", "Boundary (6 days)", "Completed 6 days ago", "-", "2026-11-15 12:00", CN, "True", "True",
   PASS, priority=M)
tc("TC-WB-025", "F11", "Branch (n parameter)", "n=1, completed 2 hours ago", "-", "2026-11-21 10:00, n=1", CN,
   "True", "True", PASS, priority=L)
AU = "PUT /api/tasks/<id> via Flask test client, then read the task"
tc("TC-WB-026", "F07", "Branch (done true)", "done=true sets completed_at", "Open task", "{done: true}", AU,
   "completed_at not null", "Set", PASS, priority=M)
tc("TC-WB-027", "F07", "Branch (done false)", "done=false clears completed_at", "Done task", "{done: false}", AU,
   "completed_at null", "Cleared", PASS, priority=M)
tc("TC-WB-028", "F07", "Branch (done absent)", "Update without done keeps completed_at", "Done task",
   "{title: 'x'}", AU, "completed_at unchanged", "Unchanged", PASS, priority=M)
tc("TC-WB-029", "F07", "Branch (done true twice)", "Completing a done task keeps it done", "Done task",
   "{done: true}", AU, "done stays true; completed_at set", "As expected", PASS, priority=L)

# ---------------------------------------------------------------------------
# Week 3 - GUI (15), Accessibility (11), Compatibility (5) - manual / Selenium screenshots
# ---------------------------------------------------------------------------
GM = dict(automated=False)
SHOT = "03_Special_Testing/week 3 evidence/"
gui = [
    ("001", "NF3", "Every page has a meaningful <title> and heading", "Title + h1 on all 6 pages", PASS, "", L),
    ("002", "NF3", "Top navigation links work from every page", "All links reach the right page", PASS, "", M),
    ("003", "NF3", "Button labels describe the action", "Register, Log in, Create Task, Save Changes, Delete, Filter", PASS, "", L),
    ("004", "NF3", "Error messages are in plain language", "Plain messages on register/login/task", PASS, "", M),
    ("005", "NF3", "Required fields are marked", "required attribute on title, username, password; constraint hints shown", PASS, "", L),
    ("006", "NF3", "Browser blocks empty title (required)", "Browser prompt 'Please fill out this field'", PASS, "", M),
    ("007", "NF3", "Delete asks for confirmation", "confirm('Delete this task?') dialog shown", PASS, "", H),
    ("008", "NF3", "Each urgency label has its own badge style", "'Due Today' never appears; task due today shows red 'Overdue'", FAIL, "DEF-001", H),
    ("009", "NF3", "Done tasks visually distinct", "Strike-through, grey", PASS, "", L),
    ("010", "NF3", "Empty-state message when no tasks", "'No tasks match your filters.' shown", PASS, "", L),
    ("011", "NF3", "Confirmation after create / edit / delete", "No message; page silently reloads", FAIL, "DEF-024", M),
    ("012", "NF5", "Layout at desktop 1366x768", "Correct", PASS, "", M),
    ("013", "NF5", "Layout at tablet 768x1024", "Correct", PASS, "", M),
    ("014", "NF5", "Layout at phone 375x812", "Task list, New Task and Dashboard scroll sideways; Urgency column cut off; username cut off", FAIL, "DEF-023", H),
    ("015", "NF3", "Form keeps typed values after a validation error", "Both fields are emptied", FAIL, "DEF-025", L),
]
for n, f, obj, act, st, d, p in gui:
    tc(f"TC-GUI-{n}", f, "GUI checklist" if f == "NF3" else "Configuration (viewport)", obj,
       "App running; Chrome 153 / Linux; logged in where needed", "Seeded user and tasks",
       "1. Open each page 2. Check the item against the checklist 3. Screenshot", "Check satisfied",
       act, st, d, priority=p, automated=False,
       evidence=SHOT + ("my_tasks_phone_375x812.png" if n == "014" else f"gui_{n}.png") + "; PyTodo QA Data Collection (Week 3).xlsx")

acc = [
    ("001", "3.1.1 (A) Language of page", "<html lang='en'> on all pages", PASS, "", L),
    ("002", "2.4.2 (A) Page titled", "Unique titles", PASS, "", L),
    ("003", "1.3.1 / 4.1.2 (A) Labels", "Axe 'label' (critical): 2 inputs on Login, 2 on Register, 3 on New Task; <label> not linked to input", FAIL, "DEF-021", H),
    ("004", "4.1.2 (A) Name, role, value", "Axe 'select-name' (critical): category and status <select> have no name", FAIL, "DEF-021", H),
    ("005", "1.4.3 (AA) Contrast", "Empty-state text #999 on white = 2.8:1 (also done-task titles)", FAIL, "DEF-022", M),
    ("006", "2.1.1 (A) Keyboard", "All controls reachable by Tab", PASS, "", H),
    ("007", "2.4.7 (AA) Focus visible", "Default focus ring visible", PASS, "", M),
    ("008", "3.3.1 (A) Error identification", "Errors given as text", PASS, "", M),
    ("009", "1.4.1 (A) Use of colour", "Urgency badges have text as well as colour", PASS, "", M),
    ("010", "1.4.10 (AA) Reflow", "Horizontal scroll at 320 CSS px; Urgency column hidden", FAIL, "DEF-023", M),
    ("011", "4.1.2 / 2.4.6 (A/AA) Button names", "Button text is only the symbol 'o' or check; a screen reader announces 'white circle'", FAIL, "DEF-021", M),
]
for n, crit, act, st, d, p in acc:
    tc(f"TC-ACC-{n}", "NF4", "Accessibility (WCAG 2.1)", f"WCAG {crit} satisfied", "App running; Chrome + axe-core",
       "All 6 pages", "1. Run 03_Special_Testing/scripts/axe_scan.py 2. Manual keyboard / contrast check",
       f"No violation of {crit}", act, st, d, priority=p, automated=False,
       evidence="03_Special_Testing/axe_results/ ; PyTodo QA Data Collection (Week 3).xlsx")

comp = [("001", "Chrome 153 / Linux", PASS, "Cloud verification run (headless Chrome 153): desktop and tablet pass; phone fails (see TC-GUI-014)"),
        ("002", "Chrome 158 / Windows 11", PASS, "Chrome 158.0.8127.89 on Windows 11: smoke set passed; Selenium 7 pass / 3 fail on DEF-001, 002, 007 (AT-005 flaky, passed on re-run); desktop and tablet OK; phone emulation shows the desktop page shrunk to unreadable text (DEF-023)"),
        ("003", "Edge 158 / Windows 11", PASS, "Edge 158.0.4370.33 on Windows 11: smoke set passed (AT-001, 003, 005, 007, 009); same defects as Chrome (DEF-001, 002, 007); desktop and tablet layout OK; phone emulation shows the desktop page shrunk to unreadable text (DEF-023)"),
        ("004", "Firefox 161 / Windows 11", PASS, "Firefox 161.0 on Windows 11: smoke set passed; Selenium 7 pass / 3 fail on DEF-001, 002, 007; desktop and tablet OK; phone width: table wider than the window, sideways scroll, Delete link cut off (DEF-023)")]
# Safari / macOS was removed from scope: no member has a Mac (see residual risk R-10).
for n, env, st, act in comp:
    tc(f"TC-COMP-{n}", "NF5", "Compatibility", f"Smoke set works on {env}", f"{env}; app reachable",
       "Smoke set: register, login, create, complete, filter, dashboard, logout",
       "1. run_browser_tests.bat <browser> (10 Selenium tests incl. smoke set) 2. capture_screenshots.py at 3 viewports",
       "All smoke steps pass",
       act, st, priority=H if n in ("001", "002") else M, automated=False,
       evidence={"001": "03_Special_Testing/week 3 evidence/ (cloud screenshots)",
                 "002": "03_Special_Testing/week 3 evidence/chrome/; 06_Automation_Regression/week 6 evidence/chrome_windows_run_summary.txt",
                 "003": "03_Special_Testing/week 3 evidence/edge/; 06_Automation_Regression/week 6 evidence/edge_run_summary.txt",
                 "004": "03_Special_Testing/week 3 evidence/firefox/; 06_Automation_Regression/week 6 evidence/firefox_run_summary.txt"}[n])

# ---------------------------------------------------------------------------
# Week 4 - API (46)
# ---------------------------------------------------------------------------
A = "Send request with Flask test client; check status and JSON body"
api = [
    ("001", "F01", "Functional (valid)", "Register valid user", "POST /api/register {username:'api_ok', password:'Passw0rd!'}", "201; {id, username}", "201 {id, username}", PASS, "", H, True),
    ("002", "F01", "Negative (invalid username)", "Short username rejected", "{username:'ab', password:'Passw0rd!'}", "400 with error", "400", PASS, "", M, False),
    ("003", "F01", "Negative (invalid password)", "Short password rejected", "{username:'api_pw', password:'short'}", "400 with error", "400", PASS, "", M, False),
    ("004", "F01", "Negative (missing data)", "Missing fields rejected", "{}", "400", "400", PASS, "", M, False),
    ("005", "F01", "Negative (duplicate)", "Duplicate username rejected", "register 'api_dup' twice", "Second call 400/409 'username taken'", "HTTP 201, body {'id': 2, 'username': 'api_dup'}", FAIL, "DEF-004", H, True),
    ("006", "F01", "Negative (wrong type)", "Number as username rejected cleanly", "{username: 12345, password:'Passw0rd!'}", "400 (not 500)", "HTTP 500 Internal Server Error (HTML)", FAIL, "DEF-018", M, False),
    ("007", "F02", "Functional (valid)", "Login valid", "POST /api/login qa_user1", "200; session cookie", "200", PASS, "", H, True),
    ("008", "F02", "Negative", "Wrong password", "qa_user1 / WrongPass1", "401", "401", PASS, "", H, False),
    ("009", "F02", "Negative", "Unknown user", "ghost / Passw0rd!", "401", "401", PASS, "", M, False),
    ("010", "F03", "Negative (no session)", "Task list needs login", "GET /api/tasks without login", "401", "401", PASS, "", H, False),
    ("011", "F12", "Negative (no session)", "Categories need login (README: all except register/login)", "GET /api/categories without login", "401", "HTTP 200, body [{'id':1,'name':'Work'}, ...]", FAIL, "DEF-016", L, False),
    ("012", "F12", "Functional", "Categories listed when logged in", "GET /api/categories", "200; Work, Personal, Study, Urgent", "200; 4 categories", PASS, "", L, False),
    ("013", "F04", "Functional (valid)", "Create task with all fields", "{title:'API task', category_id:1, due_date: today+3}", "201; task JSON", "201", PASS, "", H, True),
    ("014", "F04", "Functional (title only)", "Create task with title only", "{title:'Only title'}", "201", "201", PASS, "", M, False),
    ("015", "F04", "Negative (missing data)", "Missing title rejected", "{category_id:1}", "400 'title is required'", "400", PASS, "", H, False),
    ("016", "F04", "Negative (wrong type)", "Number as title handled cleanly", "{title: 123}", "400 or 201 with title '123' (not 500)", "HTTP 500 Internal Server Error", FAIL, "DEF-018", M, False),
    ("017", "F04", "Negative (invalid date)", "Impossible date rejected", "{title:'x', due_date:'2026-13-45'}", "400; task not stored", "HTTP 500 Internal Server Error", FAIL, "DEF-008", H, True),
    ("018", "F04", "Negative (wrong format)", "Wrong date format rejected", "{title:'x', due_date:'21/11/2026'}", "400; task not stored", "HTTP 500 Internal Server Error", FAIL, "DEF-008", H, False),
    ("019", "F04", "Negative (unknown reference)", "Unknown category id rejected", "{title:'x', category_id: 999}", "400", "HTTP 201, category None, category_id 999", FAIL, "DEF-011", L, False),
    ("020", "F04", "Negative (wrong content type)", "Non-JSON body gets a clear error", "text/plain body 'hello'", "400/415 saying body must be JSON", "HTTP 400 {'error': 'title is required'}", FAIL, "DEF-017", L, False),
    ("021", "F04", "Edge (very long)", "Very long title limited", "{title: 'a'*5000}", "400 (documented maximum length)", "HTTP 201; 5,000-character title stored", FAIL, "DEF-013", L, False),
    ("022", "F05", "Functional", "Get own task by id", "GET /api/tasks/<own id>", "200; task JSON", "200", PASS, "", H, False),
    ("023", "F05", "Negative (unknown id)", "Unknown id", "GET /api/tasks/99999", "404", "404", PASS, "", H, False),
    ("024", "F03", "Negative (other user)", "Other user's task hidden", "GET /api/tasks/<qa_user2 id> as qa_user1", "404", "404", PASS, "", H, True),
    ("025", "F05", "Functional", "List newest first", "3 tasks created in order", "200; newest first", "Newest first", PASS, "", M, False),
    ("026", "F05", "Functional (pagination)", "page=0, per_page=2 returns 2", "5 tasks", "200; 2 items", "2 items", PASS, "", M, False),
    ("027", "F05", "Negative (pagination)", "Negative page rejected", "?page=-1", "400", "HTTP 200 with tasks", FAIL, "DEF-012", L, False),
    ("028", "F05", "Negative (pagination)", "per_page=0 rejected", "?per_page=0", "400", "HTTP 200, body []", FAIL, "DEF-012", L, False),
    ("029", "F05", "Edge (pagination)", "Page beyond end returns empty list", "?page=50", "200; []", "200 []", PASS, "", L, False),
    ("030", "F09", "Functional (filter)", "Category filter", "?category=Work", "Only Work tasks", "As expected", PASS, "", M, False),
    ("031", "F09", "Functional (filter)", "Status done filter", "?status=done", "Only done tasks", "As expected", PASS, "", M, False),
    ("032", "F09", "Functional (search)", "Search partial title", "?q=repo", "'Write report' returned", "Returned", PASS, "", M, False),
    ("033", "F09", "Edge (apostrophe)", "Search with an apostrophe works like the web UI", "?q=Mum's", "200 with the task (web UI works: TC-BB-044)", "HTTP 500 Internal Server Error", FAIL, "DEF-006", H, True),
    ("034", "F06", "Functional (partial update)", "PUT title only", "{title:'Renamed'}", "200; title changed; other fields kept", "As expected", PASS, "", M, False),
    ("035", "F06", "Negative (empty)", "PUT empty title rejected", "{title:''}", "400; title unchanged", "HTTP 200; title set to ''", FAIL, "DEF-009", H, True),
    ("036", "F07", "Negative (wrong type)", "done='false' (string) not treated as true", "{done:'false'}", "400, or done stays false", "HTTP 200, done = True (task marked complete)", FAIL, "DEF-010", M, True),
    ("037", "F03", "Negative (other user)", "PUT other user's task refused", "PUT /api/tasks/<qa_user2 id>", "404", "404", PASS, "", H, False),
    ("038", "F06", "Negative (unknown id)", "PUT unknown id", "PUT /api/tasks/99999", "404", "404", PASS, "", M, False),
    ("039", "F06", "Negative (invalid date)", "PUT impossible date rejected", "{due_date:'2026-13-45'}", "400; task still readable", "HTTP 500 Internal Server Error", FAIL, "DEF-008", H, False),
    ("040", "F08", "Functional", "Delete own task", "DELETE /api/tasks/<own id>", "200; task gone", "200; gone", PASS, "", H, True),
    ("041", "F08", "Negative (unknown id)", "Delete unknown id returns 404", "DELETE /api/tasks/99999", "404", "HTTP 200, body {'result': 'ok'}", FAIL, "DEF-005", H, False),
    ("042", "F03", "Negative (other user)", "Cannot delete another user's task", "DELETE qa_user2's task as qa_user1", "404/403; qa_user2's task still exists", "HTTP 200 {'result': 'ok'} and qa_user2's task was deleted", FAIL, "DEF-005", H, True),
    ("043", "F08", "Negative (no session)", "Delete needs login", "DELETE without login", "401", "401", PASS, "", H, True),
    ("044", "F11", "Functional", "Dashboard counts", "Seeded tasks", "Correct total/open/overdue/due_soon/completed_this_week", "As expected", PASS, "", M, False),
    ("045", "F11", "Boundary (day 0)", "Task due today not counted as overdue", "One open task due today", "overdue 0", "{'overdue': 1, ...}", FAIL, "DEF-001", H, True),
    ("046", "F11", "Negative (no session)", "Dashboard needs login", "GET /api/dashboard without login", "401", "401", PASS, "", M, False),
]
for n, f, t, obj, data, exp, act, st, d, p, reg in api:
    tc(f"TC-API-{n}", f, "API - " + t, obj, "Fresh DB; qa_user1 & qa_user2 seeded (where needed)", data, A,
       exp, act, st, d, priority=p, regression=reg)

# ---------------------------------------------------------------------------
# Week 5 - Security (14, TC-SEC-013 manual) and Performance (5)
# ---------------------------------------------------------------------------
sec = [
    ("001", "F02", "Spoofing / session", "Session cookie is HttpOnly", "Login response", "Set-Cookie has HttpOnly", "HttpOnly present", PASS, "", H, False, True),
    ("002", "F03", "Spoofing / tampering", "Cookie signed with a wrong key is rejected", "Cookie signed with 'wrong-key' for user_id=2", "401 / redirect to login", "Rejected", PASS, "", H, False, True),
    ("003", "F03", "Spoofing (STRIDE S)", "Cookie cannot be forged from source code", "Cookie signed with the SECRET_KEY found in app.py, user_id=2", "Rejected", "Forged cookie accepted; qa_user2's private task read", FAIL, "DEF-014", H, True, True),
    ("004", "F02", "Spoofing (brute force)", "Repeated failed logins are limited", "20 wrong passwords then the correct one", "429 or lockout after N attempts", "All 20 answered 401; no limit; correct password then accepted", FAIL, "DEF-019", M, False, True),
    ("005", "F02", "Spoofing (session replay)", "Cookie invalid after logout", "Cookie copied before logout", "Replayed cookie rejected", "Old cookie still opens /api/tasks (200)", FAIL, "DEF-020", M, False, True),
    ("006", "F08", "Tampering (CSRF)", "State-changing form needs a CSRF token", "POST /tasks/<id>/delete without token, foreign Origin", "400/403", "Accepted; task deleted", FAIL, "DEF-015", H, True, True),
    ("007", "F03", "Tampering (authorisation)", "PUT other user's task refused", "PUT qa_user2 task as qa_user1", "404/403; unchanged", "404; unchanged", PASS, "", H, False, True),
    ("008", "F03", "Tampering / EoP", "DELETE other user's task refused", "DELETE qa_user2 task as qa_user1", "404/403; task kept", "200; task deleted", FAIL, "DEF-005", H, True, True),
    ("009", "F03", "Information disclosure", "GET other user's task refused", "GET qa_user2 task as qa_user1", "404", "404", PASS, "", H, True, True),
    ("010", "F09", "Information disclosure (SQL injection)", "Search input cannot change the SQL query", "q = x%' OR user_id != 0 OR title LIKE '%", "Only own tasks (or none)", "qa_user2's task returned", FAIL, "DEF-006", H, True, True),
    ("011", "F01", "Information disclosure (storage)", "Passwords stored hashed", "Read users table", "Salted hash, not plain text", "scrypt hash", PASS, "", H, False, True),
    ("012", "F05", "Tampering (stored XSS)", "Script in title is escaped", "title = <script>alert(1)</script>", "Shown as text (&lt;script&gt;)", "Raw <script> rendered in page", FAIL, "DEF-007", H, True, True),
    ("013", "F04", "Information disclosure (debug)", "Server errors do not expose debugger", "Trigger 500 via invalid date (DEF-008) in browser", "Generic 500 page", "Werkzeug Debugger with traceback and paths", FAIL, "DEF-014", H, False, False),
    ("014", "F03", "Elevation of privilege", "Edit page of another user's task refused", "GET /tasks/<qa_user2 id>/edit as qa_user1", "404/403 or redirect", "Redirected to My Tasks (302); task not shown", PASS, "", H, False, True),
]
for n, f, t, obj, data, exp, act, st, d, p, reg, auto in sec:
    tc(f"TC-SEC-{n}", f, "Security - " + t, obj, "Local copy only; fresh temp DB; qa_user1 & qa_user2",
       data, "Run the scripted request (see test_security.py)" if auto else
       "1. Start app with python app.py 2. Create task with due 2026-13-45 via API 3. Open / in browser 4. Screenshot",
       exp, act, st, d, priority=p, regression=reg, automated=auto,
       evidence=None if auto else "05_Security_Performance/week 5 evidence/werkzeug_debugger.png (manual)")

perf = [("001", 1, "Task list p95 5 ms, dashboard 6 ms, login 120 ms; 0 errors", PASS, ""),
        ("002", 10, "Task list p95 6 ms, dashboard 11 ms, login 610 ms; 0 errors", PASS, ""),
        ("003", 25, "Login p95 1,200 ms (> 1,000 ms); others < 10 ms; 0 errors", FAIL, "DEF-026"),
        ("004", 50, "Login p95 2,500 ms; task list 9 ms; dashboard 12 ms; 0 errors", FAIL, "DEF-026"),
        ("005", 100, "Stress, ramp 10/s: login p95 560 ms; task list 16 ms; dashboard 45 ms; 0 errors", PASS, "")]
for n, u, act, st, d in perf:
    tc(f"TC-PERF-{n}", "NF2", "Performance (load)" if u < 100 else "Performance (stress)",
       f"p95 < 1,000 ms and 0% errors at {u} user(s)", "Dev server, debug on, SQLite, 2 vCPU / 8 GB; perf_user with 100 tasks",
       f"{u} users; 60% GET /api/tasks, 30% GET /api/dashboard, 10% POST /api/tasks; think 1-2 s; 40 s",
       f"locust -f locustfile.py --headless -u {u} -r {u if u < 100 else 10} -t 40s --csv results/u{u}",
       "p95 < 1,000 ms; 0% errors for every request type", act, st, d,
       priority=M if u < 100 else L, automated=False,
       evidence=f"05_Security_Performance/performance/results/u{u}_stats.csv")

# ---------------------------------------------------------------------------
# Week 6 - Selenium UI automation (10)
# ---------------------------------------------------------------------------
ats = [
    ("001", "F01", "Register and land on My Tasks", "TC-BB-002, TC-BB-013", "My Tasks shown", "As expected", PASS, "", H, True),
    ("002", "F01", "8-character password accepted", "TC-BB-010", "Account created", "Password error shown", FAIL, "DEF-002", H, True),
    ("003", "F02", "Login, logout, protected page", "TC-BB-017, TC-BB-038", "Login works; after logout / redirects to login", "As expected", PASS, "", H, True),
    ("004", "F10", "Due-today badge", "TC-BB-026", "'Due Today'", "'Overdue'", FAIL, "DEF-001", H, True),
    ("005", "F07", "Complete and reopen", "TC-BB-032, TC-BB-033", "Done then open", "As expected", PASS, "", M, False),
    ("006", "F08", "Delete with confirm dialog", "TC-BB-034, TC-GUI-007", "Dialog; task removed", "As expected", PASS, "", M, False),
    ("007", "F09", "Category filter", "TC-BB-039", "Only Work tasks", "As expected", PASS, "", M, False),
    ("008", "F04", "HTML in title not rendered", "TC-BB-024, TC-SEC-012", "Literal text '<b>bold</b>' visible", "Text rendered as bold HTML", FAIL, "DEF-007", H, False),
    ("009", "F11", "Dashboard counters", "TC-BB-045", "Counters match", "As expected", PASS, "", M, False),
    ("010", "NF3", "Browser blocks empty title", "TC-GUI-006", "Form not submitted", "As expected", PASS, "", L, False),
]
for n, f, obj, maps, exp, act, st, d, p, reg in ats:
    tc(f"AT-{n}", f, "UI automation (Selenium, POM)", obj, "App running at BASE_URL; Chrome/Edge/Firefox driver",
       "Generated unique user per test", f"Automates {maps}", exp, act, st, d, priority=p, regression=reg)

AT_MAP = {f"AT-{n}": maps for n, f, obj, maps, *_ in ats}

# ---------------------------------------------------------------------------
# Defects (Defect Report Template)
# ---------------------------------------------------------------------------
ENV = "Python 3.13, Flask 3.0.3, Werkzeug 3.x, SQLite; Linux; Chrome 153; fresh temp DB"
DEFECTS = []


def defect(id_, title, feature, area, sev, pri, pre, steps, exp, act, evidence):
    DEFECTS.append(OrderedDict([
        ("Defect ID", id_), ("Title", title), ("Affected Feature", feature), ("Area", area),
        ("Environment", ENV), ("Preconditions", pre), ("Steps to Reproduce", steps),
        ("Expected Result", exp), ("Actual Result", act), ("Severity", sev), ("Priority", pri),
        ("Evidence", evidence), ("Status", "Confirmed"),
    ]))


defect("DEF-001", "Task due today is labelled 'Overdue' instead of 'Due Today'", "F10 Urgency / F11 Dashboard",
       "Business logic", "Major", "High", "Logged in", "1. Create task due today 2. Open My Tasks 3. Open Dashboard",
       "Badge 'Due Today'; Overdue counter 0", "Badge 'Overdue'; Overdue = 1 (helpers.compute_urgency uses due <= today)",
       "TC-BB-026, TC-BB-046, TC-WB-004, TC-API-045, TC-GUI-008, AT-004")
defect("DEF-002", "Password of exactly 8 characters is rejected", "F01 Registration", "Input validation", "Major", "High",
       "Logged out", "1. Register with password 'Abcd123!' (8 chars)", "Account created",
       "'Password must be at least 8 characters.' (is_valid_password uses len > 8)", "TC-BB-010, TC-WB-010, AT-002")
defect("DEF-003", "Task completed exactly 7 days ago is not counted in 'Completed (last 7 days)'", "F11 Dashboard",
       "Business logic", "Moderate", "Medium", "Task completed exactly 7 days ago",
       "1. Call completed_in_last_n_days with age 7 days 2. Compare with dashboard", "Counted (inclusive window)",
       "Not counted (age.days < n)", "TC-WB-021")
defect("DEF-004", "Duplicate usernames are accepted; the second account can never log in", "F01 Registration / F02 Login",
       "Input validation", "Major", "High", "'dt_taken' exists", "1. Register 'dt_taken' again 2. Log in with second password",
       "Refused with 'username already taken'", "Second account created (302 / 201); it can never log in",
       "TC-BB-014, TC-BB-020, TC-API-005")
defect("DEF-005", "Any logged-in user can delete another user's task through the API", "F08 Delete / F03 Access control",
       "Security", "Critical", "High", "qa_user2 owns a task",
       "1. Log in as qa_user1 2. DELETE /api/tasks/<qa_user2 task id> 3. qa_user2 opens the task",
       "404/403; task kept. Unknown id gives 404", "200 {'result':'ok'}; qa_user2's task is gone. Unknown id also gives 200",
       "TC-API-041, TC-API-042, TC-SEC-008")
defect("DEF-006", "SQL injection in API search parameter q leaks other users' tasks", "F09 Search", "Security",
       "Critical", "High", "qa_user1 and qa_user2 each own a task",
       "1. Log in as qa_user1 2. GET /api/tasks?q=x%' OR user_id != 0 OR title LIKE '% 3. GET /api/tasks?q=Mum's",
       "Only own tasks; apostrophe search works", "qa_user2's task returned; apostrophe gives HTTP 500",
       "TC-SEC-010, TC-API-033")
defect("DEF-007", "Task title is rendered as raw HTML (stored XSS)", "F04 Create / F05 List", "Security", "Critical", "High",
       "Logged in", "1. Create task titled <script>alert(1)</script> 2. Open My Tasks", "Title shown as text",
       "Script tag rendered (template uses |safe)", "TC-BB-024, TC-SEC-012, AT-008")
defect("DEF-008", "Invalid due date is saved and then breaks My Tasks, the API list and the Dashboard (HTTP 500)",
       "F04 Create / F06 Edit", "Input validation", "Critical", "High", "Logged in",
       "1. POST task with due_date 2026-13-45 2. Open My Tasks / GET /api/tasks / Dashboard",
       "400; task not stored; pages still load", "Task stored; every list page returns 500 permanently for that user",
       "TC-BB-049, TC-API-017, TC-API-018, TC-API-039; root cause characterised by TC-WB-008 (pass)")
defect("DEF-009", "Empty title accepted (web form with spaces, API PUT with \"\")", "F04 Create / F06 Edit",
       "Input validation", "Moderate", "Medium", "Logged in; task exists",
       "1. POST /tasks/new title='   ' 2. PUT /api/tasks/<id> {title:''}", "400 / form error; title kept",
       "Blank task created; title set to ''", "TC-BB-023, TC-BB-048, TC-API-035")
defect("DEF-010", "PUT with done: \"false\" (string) marks the task as done", "F07 Complete", "Input validation",
       "Moderate", "Medium", "Open task", "1. PUT /api/tasks/<id> {done:'false'}", "400, or task stays open",
       "200; done = true", "TC-API-036")
defect("DEF-011", "Task can be created with a category id that does not exist", "F04 Create", "Input validation",
       "Minor", "Low", "Logged in", "1. POST /api/tasks {title:'x', category_id:999}", "400", "201; category None",
       "TC-API-019")
defect("DEF-012", "Invalid pagination values accepted (page=-1, per_page=0); page numbering (starts at 0) not documented",
       "F05 List", "API", "Minor", "Low", "Tasks exist", "1. GET /api/tasks?page=-1 2. GET /api/tasks?per_page=0", "400",
       "200 with tasks / 200 []", "TC-API-027, TC-API-028")
defect("DEF-013", "No maximum length for task title (5,000 characters accepted)", "F04 Create", "Input validation",
       "Minor", "Low", "Logged in", "1. POST /api/tasks with 5,000-char title", "400 with documented limit", "201",
       "TC-API-021")
defect("DEF-014", "Secret key is hard-coded and the app runs in debug mode (session forgery, debugger exposed)",
       "F03 Access control", "Security", "Critical", "High", "Source code available (app.py)",
       "1. Sign a session cookie for user_id=2 with the SECRET_KEY in app.py 2. GET /api/tasks 3. Trigger any 500 in browser",
       "Forged cookie rejected; generic error page", "qa_user2's tasks returned; Werkzeug Debugger shown",
       "TC-SEC-003, TC-SEC-013")
defect("DEF-015", "No CSRF protection on state-changing forms", "F08 Delete / F07 Toggle", "Security", "Major", "Medium",
       "Victim logged in", "1. From another origin, POST /tasks/<id>/delete without token", "403", "Task deleted",
       "TC-SEC-006")
defect("DEF-016", "/api/categories works without logging in", "F12 Categories", "API", "Minor", "Low", "Logged out",
       "1. GET /api/categories", "401", "200 with list", "TC-API-011")
defect("DEF-017", "Non-JSON request body gets a misleading error", "F04 Create", "API", "Minor", "Low", "Logged in",
       "1. POST /api/tasks text/plain 'hello'", "400/415 'body must be JSON'", "400 'title is required'", "TC-API-020")
defect("DEF-018", "Wrong JSON data types crash the server (HTTP 500)", "F01 Register / F04 Create", "Input validation",
       "Moderate", "Medium", "-", "1. POST /api/register {username:12345} 2. POST /api/tasks {title:123}", "400",
       "500", "TC-API-006, TC-API-016")
defect("DEF-019", "No limit on failed login attempts (brute force possible)", "F02 Login", "Security", "Moderate",
       "Medium", "qa_user1 exists", "1. POST wrong password 20 times", "Lockout / 429", "All accepted for checking",
       "TC-SEC-004")
defect("DEF-020", "Session cookie still works after logout", "F02 Logout", "Security", "Moderate", "Medium",
       "Logged in", "1. Copy cookie 2. Log out 3. Replay cookie", "401", "200", "TC-SEC-005")
defect("DEF-021", "Form fields, filter dropdowns and the complete button have no accessible name", "NF4 Accessibility",
       "GUI / accessibility", "Major", "Medium", "-", "1. Run axe on Login, Register, New Task, My Tasks",
       "No critical violations", "'label', 'select-name' critical; button named 'white circle'",
       "TC-ACC-003, TC-ACC-004, TC-ACC-011")
defect("DEF-022", "Low colour contrast for grey text (#999 on white = 2.8:1)", "NF4 Accessibility",
       "GUI / accessibility", "Minor", "Low", "-", "1. Measure contrast of empty-state and done-task text",
       ">= 4.5:1", "2.8:1", "TC-ACC-005")
defect("DEF-023", "Layout breaks on phone width: sideways scrolling, Urgency column hidden", "NF5 / NF4",
       "GUI / accessibility", "Moderate", "Medium", "Viewport 375x812", "1. Open My Tasks, New Task, Dashboard",
       "No horizontal scroll; readable text", "Chrome 375 px window and Firefox 161: sideways scroll, columns cut off. Chrome 158 and Edge 158 phone emulation: desktop page shrunk to unreadable text (no viewport meta tag)", "TC-GUI-014, TC-ACC-010; index_phone.png in week 3 evidence/chrome, edge, firefox")
defect("DEF-024", "No confirmation message after create, edit or delete", "NF3 GUI", "GUI / accessibility", "Minor",
       "Low", "Logged in", "1. Create/edit/delete a task", "Success message", "Silent reload", "TC-GUI-011")
defect("DEF-025", "Register form clears both fields after a validation error", "NF3 GUI", "GUI / accessibility",
       "Minor", "Low", "-", "1. Register with short password", "Username kept", "Both fields emptied", "TC-GUI-015")
defect("DEF-026", "Login slows above 1 s when 25+ users log in at the same moment", "NF2 Performance", "Performance",
       "Minor", "Low", "perf_user; Locust", "1. Run locust -u 25 -r 25", "p95 < 1,000 ms", "p95 1,200 ms (25), 2,500 ms (50)",
       "TC-PERF-003, TC-PERF-004")

# ---------------------------------------------------------------------------
# Risk register (Week 1 vs final)
# ---------------------------------------------------------------------------
RISKS = [
    ("R-01", "Users can change or delete other users' data", 2, 3, 3, "DEF-005, DEF-014, DEF-015"),
    ("R-02", "Injected input changes SQL queries", 2, 3, 3, "DEF-006"),
    ("R-03", "Scripts run in other users' browsers", 2, 3, 3, "DEF-007"),
    ("R-04", "Bad input corrupts a user's data and crashes pages", 2, 3, 3, "DEF-008, DEF-009, DEF-018"),
    ("R-05", "Wrong urgency misleads users about deadlines", 2, 2, 3, "DEF-001, DEF-003"),
    ("R-06", "Valid users cannot register or log in", 2, 2, 3, "DEF-002, DEF-004"),
    ("R-07", "Accounts taken over by guessing or stolen cookies", 1, 3, 2, "DEF-019, DEF-020"),
    ("R-08", "People with disabilities cannot use the forms", 1, 2, 3, "DEF-021, DEF-022, DEF-023"),
    ("R-09", "Slow response at busy times", 1, 2, 1, "DEF-026"),
    ("R-10", "Untested browsers behave differently", 2, 1, 1, "Chrome, Edge, Firefox tested (TC-COMP-001-004); Safari out of scope"),
]

# Requirement -> test scenario text for the RTM template
SCENARIOS = {
    "F01": "Valid/invalid account creation; username & password boundaries; duplicate username",
    "F02": "Valid/invalid authentication; logout; brute force; session replay",
    "F03": "Logged-out redirect/401; cross-user GET/PUT/DELETE; cookie forgery",
    "F04": "Create with valid/invalid title, date, category, types; XSS in title",
    "F05": "List order; pagination; get by id; output encoding",
    "F06": "Edit fields; partial update; empty title; invalid date",
    "F07": "Complete/reopen state transitions; completed_at; done type",
    "F08": "Owner delete; unknown id; CSRF; no session",
    "F09": "Category/status filters; partial search; apostrophe; SQL injection",
    "F10": "Boundary around due-date classification (day -1, 0, 1, 2, 3); none; done",
    "F11": "Dashboard counters; due-today; 7-day completed window",
    "F12": "Category list with/without session",
    "NF2": "Response time, throughput, errors at 1/10/25/50/100 users",
    "NF3": "Checklist of forms, buttons, messages, navigation, feedback",
    "NF4": "WCAG 2.1 A/AA checks with axe-core and keyboard",
    "NF5": "Chrome, Edge, Firefox (Windows) and Chrome (Linux) x 3 viewports; smoke set",
}


def summary():
    from collections import Counter
    st = Counter(t["Status"] for t in TEST_CASES)
    return len(TEST_CASES), st


if __name__ == "__main__":
    n, st = summary()
    print(n, dict(st))
