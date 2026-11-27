"""
qa_support.py - shared helpers used by every PyTest suite.

* load_app()      : imports the UNMODIFIED PyTodo Pro from ./app and points it at a
                    fresh temporary SQLite file (independence: we never edit app code).
* Web helpers     : register / login / create task through the HTML forms.
* API helpers     : thin wrappers around the JSON API.
* Unit adapters   : call helpers.py functions even if parameter names differ.
"""
import html as html_lib
import importlib
import inspect
import os
import re
import sys
from datetime import date, datetime, timedelta

import qa_config as C

if C.APP_DIR not in sys.path:
    sys.path.insert(0, C.APP_DIR)


# ---------------------------------------------------------------------------
# Application loading with a fresh database
# ---------------------------------------------------------------------------
def load_app(db_path):
    """Return (flask_app, module) using db_path as the SQLite database."""
    for var in C.DB_ENV_VARS:
        os.environ[var] = db_path
    cwd = os.getcwd()
    os.chdir(C.APP_DIR)          # relative paths in app.py (templates, db) resolve
    try:
        mod = importlib.import_module(C.APP_MODULE)
        for attr in C.DB_MODULE_ATTRS:
            if hasattr(mod, attr):
                setattr(mod, attr, db_path)
        obj = getattr(mod, C.APP_OBJECT, None)
        if obj is None or callable(obj) and not hasattr(obj, "test_client"):
            factory = getattr(mod, "create_app")
            try:
                obj = factory({"TESTING": True, "DATABASE": db_path})
            except TypeError:
                obj = factory()
        flask_app = obj
        flask_app.config["TESTING"] = True
        flask_app.config["PROPAGATE_EXCEPTIONS"] = False   # a crash is observed as HTTP 500, as a user sees it
        for key in C.DB_CONFIG_KEYS:
            flask_app.config[key] = db_path
        with flask_app.app_context():
            for fn in C.DB_INIT_FUNCS:
                if hasattr(mod, fn):
                    _call_flexible(getattr(mod, fn), db_path)
                    break
    finally:
        os.chdir(cwd)
    return flask_app, mod


def _call_flexible(fn, db_path):
    try:
        sig = inspect.signature(fn)
        if len(sig.parameters) == 0:
            return fn()
        return fn(db_path)
    except TypeError:
        return fn()


def helpers():
    return importlib.import_module(C.HELPERS_MODULE)


# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------
def day(offset=0):
    """ISO date relative to the run date, so tests behave the same on any day."""
    return (date.today() + timedelta(days=offset)).isoformat()


def unique(prefix="u"):
    return f"{prefix}{datetime.now().strftime('%H%M%S%f')[-9:]}"


# ---------------------------------------------------------------------------
# Web (HTML form) helpers
# ---------------------------------------------------------------------------
def route(name, **kw):
    return C.ROUTES[name].format(**kw)


def web_register(client, username, password=C.PASSWORD, follow=False):
    return client.post(route("register"), data={C.F_USERNAME: username, C.F_PASSWORD: password},
                       follow_redirects=follow)


def web_login(client, username, password=C.PASSWORD, follow=False):
    return client.post(route("login"), data={C.F_USERNAME: username, C.F_PASSWORD: password},
                       follow_redirects=follow)


def web_logout(client):
    if C.LOGOUT_METHOD.upper() == "POST":
        return client.post(route("logout"))
    return client.get(route("logout"))


def web_new_task(client, title, category_id="", due=""):
    return client.post(route("new_task"), data={C.F_TITLE: title, C.F_CATEGORY: category_id, C.F_DUE: due})


def page(client, name="index", query=None, **kw):
    return client.get(route(name, **kw), query_string=query or {})


def text(resp):
    return resp.get_data(as_text=True)


def visible_text(html):
    """Strip tags and unescape entities -> what the user reads."""
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    return re.sub(r"\s+", " ", html_lib.unescape(re.sub(r"<[^>]+>", " ", html))).strip()


def row_html(html, needle):
    """Return the table row (or nearby block) of the task whose title contains needle."""
    for chunk in re.split(r"(?i)<tr[\s>]", html):
        if needle in chunk or html_lib.escape(needle) in chunk:
            return chunk.split("</tr>")[0]
    i = html.find(needle)
    return html[max(0, i - 200): i + 800] if i >= 0 else ""


def dashboard_counts_from_html(html):
    t = visible_text(html)
    out = {}
    for key, label in C.DASH_LABELS.items():
        if C.DASH_NUMBER_POSITION == "after":
            m = re.search(re.escape(label) + r"(?:\s*\([^)]*\))?[^0-9]{0,40}?(\d+)", t)
        else:
            m = re.search(r"(\d+)\s*" + re.escape(label), t)
        out[key] = int(m.group(1)) if m else None
    return out


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------
def api(name, **kw):
    return C.API[name].format(**kw)


def api_register(client, username, password=C.PASSWORD):
    return client.post(api("register"), json={"username": username, "password": password})


def api_login(client, username, password=C.PASSWORD):
    return client.post(api("login"), json={"username": username, "password": password})


def signup(client, username, password=C.PASSWORD):
    """Register + log in through the API (setup only, not under test)."""
    api_register(client, username, password)
    r = api_login(client, username, password)
    assert r.status_code == 200, f"setup login failed for {username}: {r.status_code}"
    return r


def api_create(client, title="Task", category_id=None, due=None, **extra):
    body = {C.K_TITLE: title}
    if category_id is not None:
        body[C.K_CAT_ID] = category_id
    if due is not None:
        body[C.K_DUE] = due
    body.update(extra)
    return client.post(api("tasks"), json=body)


def create_task_id(client, title="Task", **kw):
    r = api_create(client, title, **kw)
    assert r.status_code in (200, 201), f"setup: could not create task ({r.status_code})"
    return r.get_json()[C.K_ID]


def api_tasks(client, **query):
    return client.get(api("tasks"), query_string=query)


def find_task(client, title):
    r = api_tasks(client, per_page=1000)
    for t in r.get_json() or []:
        if t.get(C.K_TITLE) == title:
            return t
    return None


def category_id(client, name):
    r = client.get(api("categories"))
    for c in r.get_json() or []:
        if c.get("name") == name:
            return c["id"]
    return C.CATEGORIES.index(name) + 1


def is_server_error(resp):
    return resp.status_code >= 500


# ---------------------------------------------------------------------------
# Unit adapters for helpers.py (tolerate different parameter names / return types)
# ---------------------------------------------------------------------------
def _label(result):
    if isinstance(result, (tuple, list)):
        return result[0]
    if isinstance(result, dict):
        return result.get("label") or result.get("text")
    return result


ALIASES = {
    "today": ["today", "ref_date", "reference", "as_of", "on_date", "current"],
    "n": ["n", "days", "window", "n_days"],
    "now": ["now", "ref", "reference", "as_of", "current", "today"],
}


def _call(fn, positional, by_name):
    """Call fn with positional args plus optional args matched by known names."""
    params = list(inspect.signature(fn).parameters)
    kwargs, unmatched = {}, []
    for want, value in by_name.items():
        hit = next((p for p in ALIASES.get(want, [want]) if p in params), None)
        if hit:
            kwargs[hit] = value
        else:
            unmatched.append(value)
    return fn(*positional, *unmatched, **kwargs)


def compute_urgency(due, today=None):
    fn = helpers().compute_urgency
    return _label(_call(fn, [due], {"today": today} if today is not None else {}))


def is_valid_password(pw):
    return bool(helpers().is_valid_password(pw))


def is_valid_username(name):
    return bool(helpers().is_valid_username(name))


def completed_in_last_n_days(completed_at, n=7, now=None):
    """completed_at / now are datetimes; converted to the app's stored text format."""
    fn = helpers().completed_in_last_n_days
    if isinstance(completed_at, datetime):
        completed_at = completed_at.strftime(C.COMPLETED_AT_FORMAT)
    extra = {"n": n}
    if now is not None:
        extra["now"] = now
    return bool(_call(fn, [completed_at], extra))
