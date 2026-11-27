"""
Root conftest: fixtures shared by every suite + a small results recorder.

Independence rules (Test Plan section 5):
  * every test gets a brand-new temporary SQLite database;
  * the application code in ./app is imported, never modified;
  * tests do not depend on each other or on execution order.
"""
import json
import os
import re

import pytest

import qa_config as C
import qa_support as S

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(ROOT, "reports")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def app_db(tmp_path):
    """(flask_app, module, db_path) with a fresh database."""
    db_path = str(tmp_path / "pytodo_test.db")
    flask_app, mod = S.load_app(db_path)
    return flask_app, mod, db_path


@pytest.fixture
def app(app_db):
    return app_db[0]


@pytest.fixture
def client(app):
    """Logged-out client."""
    return app.test_client()


@pytest.fixture
def user1(app):
    """Client logged in as qa_user1."""
    c = app.test_client()
    S.signup(c, C.USER1)
    return c


@pytest.fixture
def user2(app):
    """Client logged in as qa_user2."""
    c = app.test_client()
    S.signup(c, C.USER2)
    return c


# ---------------------------------------------------------------------------
# Markers and result recording
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Evidence recorder (QA_EVIDENCE=1): logs every request/response a test makes
# to the real app, so tools/capture_week_evidence.py can screenshot it.
# ---------------------------------------------------------------------------
EVIDENCE = os.environ.get("QA_EVIDENCE") == "1"
_exchanges = []


@pytest.fixture(autouse=True)
def _record_exchanges(monkeypatch):
    if not EVIDENCE:
        yield
        return
    from flask.testing import FlaskClient
    original = FlaskClient.open

    who = {}

    def recording_open(self, *args, **kwargs):
        resp = original(self, *args, **kwargs)
        try:
            payload = kwargs.get("json") or kwargs.get("data")
            if isinstance(payload, dict) and "username" in payload and resp.status_code in (200, 201, 302):
                if "/register" in str(args[:1]) or "/login" in str(args[:1]):
                    who[id(self)] = payload["username"]
            req = resp.request
            if "json" in kwargs:
                body = json.dumps(kwargs["json"])
            elif "data" in kwargs:
                body = kwargs["data"] if isinstance(kwargs["data"], str) else json.dumps(kwargs["data"])
            else:
                body = ""
            _exchanges.append({"user": who.get(id(self), "anonymous"), "method": req.method if req is not None else "?",
                               "url": (req.path + ("?" + req.query_string.decode() if req.query_string else "")) if req is not None else str(args[:1]),
                               "body": body[:600], "status": resp.status_code,
                               "type": resp.content_type or "",
                               "location": resp.headers.get("Location", ""),
                               "text": resp.get_data(as_text=True)[:20000]})
        except Exception:  # never let evidence break a test
            pass
        return resp

    _exchanges.clear()
    monkeypatch.setattr(FlaskClient, "open", recording_open)
    yield


def pytest_configure(config):
    config.addinivalue_line("markers", "defect(id): known defect this test confirms when it fails")
    config._qa_results = {}


def _case_id(item):
    m = re.search(r"test_(tc_[a-z]+_\d{3}|at_\d{3})", item.name)
    return m.group(1).upper().replace("_", "-") if m else None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    cid = _case_id(item)
    if not cid:
        return
    marker = item.get_closest_marker("defect")
    if marker:
        item.user_properties.append(("defect", marker.args[0]))
    res = item.config._qa_results
    if rep.when == "setup" and rep.failed:
        res[cid] = {"status": "Blocked", "detail": str(rep.longrepr)[-400:]}
    elif rep.when == "call":
        status = "Pass" if rep.passed else "Fail"
        detail = ""
        if rep.failed:
            msg = getattr(rep.longrepr, "reprcrash", None)
            detail = msg.message if msg else str(rep.longrepr)[-400:]
        res[cid] = {"status": status, "detail": detail,
                    "defect": marker.args[0] if marker else ""}
        if EVIDENCE:
            res[cid]["exchanges"] = list(_exchanges)


def pytest_sessionfinish(session, exitstatus):
    res = getattr(session.config, "_qa_results", {})
    if not res or hasattr(session.config, "workerinput"):
        return
    os.makedirs(REPORT_DIR, exist_ok=True)
    path = os.path.join(REPORT_DIR, "evidence.json" if EVIDENCE else "results.json")
    old = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            old = json.load(fh)
    old.update(res)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(old, fh, indent=2, sort_keys=True)
