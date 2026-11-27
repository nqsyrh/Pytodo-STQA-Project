"""
qa_config.py - the ONE place to adapt the test suites to your copy of PyTodo Pro.

All suites (black-box, white-box, API, security, Selenium, Locust) read routes,
form-field names, JSON keys and test users from here.  If your lecturer's copy
uses a different route or field name, change it here only - never inside a test.

Run `pytest tests_smoke_config.py -v` first: it checks that every route below
exists in your app and tells you which ones to fix.
"""
import os

# --- Where the application under test lives ------------------------------
APP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")
APP_MODULE = "app"            # app/app.py
APP_OBJECT = "app"            # the Flask object inside app.py (or a create_app factory)
HELPERS_MODULE = "helpers"    # app/helpers.py

# How the app finds its SQLite file.  The fixture tries each of these so that
# every test gets a fresh temporary database (the original DB is never touched).
DB_MODULE_ATTRS = ["DATABASE", "DB_PATH", "DATABASE_PATH", "DB_NAME", "DB_FILE"]
DB_CONFIG_KEYS = ["DATABASE", "DB_PATH", "DATABASE_PATH"]
DB_ENV_VARS = ["PYTODO_DB", "DATABASE", "DATABASE_PATH"]
DB_INIT_FUNCS = ["init_db", "create_tables", "setup_db", "initialize_db"]

# --- Web (HTML form) routes ----------------------------------------------
ROUTES = {
    "index": "/",                         # My Tasks
    "register": "/register",
    "login": "/login",
    "logout": "/logout",
    "new_task": "/tasks/new",
    "edit_task": "/tasks/{id}/edit",
    "toggle_task": "/tasks/{id}/toggle",
    "delete_task": "/tasks/{id}/delete",
    "dashboard": "/dashboard",
}
LOGOUT_METHOD = "GET"     # change to "POST" if logout is a form button

# Form field names
F_USERNAME, F_PASSWORD = "username", "password"
F_TITLE, F_CATEGORY, F_DUE = "title", "category_id", "due_date"
# Query parameters used by the My Tasks filters (web and API)
Q_CATEGORY, Q_STATUS, Q_SEARCH = "category", "status", "q"
# The category filter (web and API) takes the category NAME, e.g. ?category=Work


# --- REST API ------------------------------------------------------------
API = {
    "register": "/api/register",
    "login": "/api/login",
    "logout": "/api/logout",
    "categories": "/api/categories",
    "tasks": "/api/tasks",
    "task": "/api/tasks/{id}",
    "dashboard": "/api/dashboard",
}
# JSON keys
K_ID, K_TITLE, K_DONE, K_DUE, K_CAT_ID, K_COMPLETED_AT = (
    "id", "title", "done", "due_date", "category_id", "completed_at")
DASH_KEYS = {"total": "total", "open": "open", "overdue": "overdue",
             "due_soon": "due_soon", "completed": "completed_this_week"}

# Text format of completed_at as stored by the app (SQLite datetime)
COMPLETED_AT_FORMAT = "%Y-%m-%d %H:%M:%S"

# Session cookie and the key the app stores the logged-in user under
SESSION_COOKIE = "session"
SESSION_USER_KEY = "user_id"

# --- Urgency labels (README) ---------------------------------------------
L_NONE, L_OVERDUE, L_TODAY, L_SOON, L_UPCOMING, L_DONE = (
    "No due date", "Overdue", "Due Today", "Due Soon", "Upcoming", "Done")

# Dashboard labels as printed on /dashboard (used to read the counters)
DASH_LABELS = {"total": "Total Tasks", "open": "Open", "overdue": "Overdue",
               "due_soon": "Due Soon", "completed": "Completed (last 7 days)"}
DASH_NUMBER_POSITION = "before"  # PyTodo Pro prints the number above its label

# Categories seeded by the app
CATEGORIES = ["Work", "Personal", "Study", "Urgent"]

# --- Test users ------------------------------------------------------------
PASSWORD = "Passw0rd!"           # 9 characters, so DEF-002 does not block setup
USER1, USER2 = "qa_user1", "qa_user2"

# --- Live server for Selenium / Locust -----------------------------------
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000")
BROWSER = os.environ.get("BROWSER", "chrome")      # chrome | edge | firefox
HEADLESS = os.environ.get("HEADLESS", "1") == "1"
