"""
Week 1 - Black-box tests (49) executed through the HTML forms.

Techniques: Equivalence Partitioning, 3-value Boundary Value Analysis,
Decision tables, State transitions.  Test design and justification:
01_Black_Box/Black_Box_Test_Design.md.  Expected results were written BEFORE
execution (PyTodo QA Data Collection (Week 1).xlsx); a failing test = a confirmed defect.

Setup that is not under test (seeding users and tasks) uses the API so each
test exercises exactly one behaviour.  Dates are relative to the run date.
"""
from urllib.parse import urlparse

import pytest

import qa_config as C
import qa_support as S

pytestmark = pytest.mark.blackbox
REG = pytest.mark.regression


def registered(client, username, password=C.PASSWORD):
    """True when the account exists (can log in through the API)."""
    S.web_logout(client)
    return S.api_login(client, username, password).status_code == 200


def redirected_home(resp):
    if resp.status_code not in (301, 302, 303):
        return False
    return urlparse(resp.headers["Location"]).path.rstrip("/") == C.ROUTES["index"].rstrip("/")


# ---------------------------------------------------------------- F01 usernames
def test_tc_bb_001(client):
    """BVA: username length 2 rejected."""
    S.web_register(client, "ab")
    assert not registered(client, "ab")


@REG
def test_tc_bb_002(client):
    """BVA: username length 3 accepted and redirected to My Tasks."""
    r = S.web_register(client, "abc")
    assert redirected_home(r), f"expected redirect to My Tasks, got {r.status_code}"
    assert registered(client, "abc")


def test_tc_bb_003(client):
    S.web_register(client, "abcd")
    assert registered(client, "abcd")


def test_tc_bb_004(client):
    S.web_register(client, "u" * 19)
    assert registered(client, "u" * 19)


@REG
def test_tc_bb_005(client):
    S.web_register(client, "u" * 20)
    assert registered(client, "u" * 20)


def test_tc_bb_006(client):
    S.web_register(client, "u" * 21)
    assert not registered(client, "u" * 21)


def test_tc_bb_007(client):
    S.web_register(client, "qa user")
    assert not registered(client, "qa user")


def test_tc_bb_008(client):
    S.web_register(client, "qa-user!")
    assert not registered(client, "qa-user!")


# ---------------------------------------------------------------- F01 passwords
@REG
def test_tc_bb_009(client):
    r = S.web_register(client, "pw_seven", "Abc123!")
    assert "at least 8 characters" in S.text(r)
    assert not registered(client, "pw_seven", "Abc123!")


@REG
@pytest.mark.defect("DEF-002")
def test_tc_bb_010(client):
    """BVA: exactly 8 characters is the minimum valid password."""
    r = S.web_register(client, "pw_eight", "Abcd123!")
    assert redirected_home(r), "DEF-002: 8-character password refused: " + S.visible_text(S.text(r))[:120]


def test_tc_bb_011(client):
    S.web_register(client, "pw_nine", "Abcd1234!")
    assert registered(client, "pw_nine", "Abcd1234!")


def test_tc_bb_012(client):
    S.web_register(client, "pw_empty", "")
    assert not registered(client, "pw_empty", "")


# ---------------------------------------------------------------- F01 decision table
@REG
def test_tc_bb_013(client):
    """R1: valid username, valid password, username free -> account created."""
    r = S.web_register(client, "dt_new")
    assert redirected_home(r) and registered(client, "dt_new")


@REG
@pytest.mark.defect("DEF-004")
def test_tc_bb_014(client):
    """R2: username already taken -> refused with a message."""
    S.web_register(client, "dt_taken")
    S.web_logout(client)
    r = S.web_register(client, "dt_taken", "Another1pass")
    assert not redirected_home(r), "DEF-004: duplicate username accepted (redirect to /)"
    assert "taken" in S.text(r).lower() or "exists" in S.text(r).lower()


def test_tc_bb_015(client):
    """R3: valid username, invalid password -> password error."""
    r = S.web_register(client, "dt_pw", "short")
    assert "password" in S.text(r).lower() and not registered(client, "dt_pw", "short")


def test_tc_bb_016(client):
    """R4: invalid username -> username error (other conditions irrelevant)."""
    r = S.web_register(client, "x")
    assert "username" in S.text(r).lower() and not registered(client, "x")


# ---------------------------------------------------------------- F02 login decision table
@REG
def test_tc_bb_017(client):
    S.api_register(client, C.USER1)
    r = S.web_login(client, C.USER1)
    assert redirected_home(r)
    assert S.page(client).status_code == 200


def test_tc_bb_018(client):
    S.api_register(client, C.USER1)
    r = S.web_login(client, C.USER1, "WrongPass1")
    assert "Invalid username or password" in S.text(r)


def test_tc_bb_019(client):
    r = S.web_login(client, "ghost")
    assert "Invalid username or password" in S.text(r)


@pytest.mark.defect("DEF-004")
def test_tc_bb_020(client):
    """Derived from R2: second 'dup_user' must be refused, or else be able to log in."""
    S.web_register(client, "dup_user", "FirstPass1")
    S.web_logout(client)
    r2 = S.web_register(client, "dup_user", "SecondPass2")
    S.web_logout(client)
    if redirected_home(r2):     # second account was created -> it must work
        r = S.web_login(client, "dup_user", "SecondPass2")
        assert redirected_home(r), "DEF-004: duplicate account created but cannot log in"


# ---------------------------------------------------------------- F04 create
@REG
def test_tc_bb_021(user1):
    cat = S.category_id(user1, "Work")
    S.web_new_task(user1, "Write report", cat, S.day(3))
    row = S.row_html(S.text(S.page(user1)), "Write report")
    assert "Work" in row and C.L_UPCOMING in row


def test_tc_bb_022(user1):
    S.web_new_task(user1, "Read book")
    row = S.row_html(S.text(S.page(user1)), "Read book")
    assert row and C.L_NONE in row


@REG
@pytest.mark.defect("DEF-009")
def test_tc_bb_023(user1):
    S.web_new_task(user1, "   ")
    tasks = S.api_tasks(user1).get_json()
    assert not any((t[C.K_TITLE] or "").strip() == "" for t in tasks), "DEF-009: blank-title task created"


@REG
@pytest.mark.defect("DEF-007")
def test_tc_bb_024(user1):
    title = "Buy milk & eggs <urgent>"
    S.web_new_task(user1, title)
    html = S.text(S.page(user1))
    assert "&lt;urgent&gt;" in html, "DEF-007: '<urgent>' inserted as raw HTML, not shown as text"


# ---------------------------------------------------------------- F10 urgency (BVA)
def badge(client, title, offset):
    S.web_new_task(client, title, "", S.day(offset) if offset is not None else "")
    return S.row_html(S.text(S.page(client)), title)


@REG
def test_tc_bb_025(user1):
    assert C.L_OVERDUE in badge(user1, "Day minus one", -1)


@REG
@pytest.mark.defect("DEF-001")
def test_tc_bb_026(user1):
    row = badge(user1, "Day zero", 0)
    assert C.L_TODAY in row, f"DEF-001: expected '{C.L_TODAY}', row shows: {S.visible_text(row)[:80]}"


@REG
def test_tc_bb_027(user1):
    assert C.L_SOON in badge(user1, "Day one", 1)


def test_tc_bb_028(user1):
    assert C.L_SOON in badge(user1, "Day two", 2)


@REG
def test_tc_bb_029(user1):
    assert C.L_UPCOMING in badge(user1, "Day three", 3)


def test_tc_bb_030(user1):
    assert C.L_NONE in badge(user1, "No date", None)


def test_tc_bb_031(user1):
    tid = S.create_task_id(user1, "Finished", due=S.day(-1))
    user1.post(S.route("toggle_task", id=tid))
    row = S.row_html(S.text(S.page(user1)), "Finished")
    assert C.L_DONE in row and C.L_OVERDUE not in row


# ---------------------------------------------------------------- F07/F08/F06 state transitions
def task_json(client, tid):
    return client.get(S.api("task", id=tid))


@REG
def test_tc_bb_032(user1):
    tid = S.create_task_id(user1, "Open task")
    user1.post(S.route("toggle_task", id=tid))
    t = task_json(user1, tid).get_json()
    assert t[C.K_DONE] and t[C.K_COMPLETED_AT]


@REG
def test_tc_bb_033(user1):
    tid = S.create_task_id(user1, "Done task")
    user1.post(S.route("toggle_task", id=tid))
    user1.post(S.route("toggle_task", id=tid))
    t = task_json(user1, tid).get_json()
    assert not t[C.K_DONE] and not t[C.K_COMPLETED_AT]


@REG
def test_tc_bb_034(user1):
    tid = S.create_task_id(user1, "Delete me")
    user1.post(S.route("delete_task", id=tid))
    assert task_json(user1, tid).status_code == 404
    assert "Delete me" not in S.text(S.page(user1))


def test_tc_bb_035(user1):
    tid = S.create_task_id(user1, "Gone")
    user1.post(S.route("delete_task", id=tid))
    r = user1.post(S.route("toggle_task", id=tid))
    assert r.status_code in (302, 303, 404) and not S.is_server_error(r)
    assert task_json(user1, tid).status_code == 404


def test_tc_bb_036(user1):
    tid = S.create_task_id(user1, "Gone too")
    user1.post(S.route("delete_task", id=tid))
    r1 = user1.get(S.route("edit_task", id=tid))
    r2 = user1.post(S.route("edit_task", id=tid), data={C.F_TITLE: "x"})
    assert r1.status_code in (302, 303, 404) and r2.status_code in (302, 303, 404)


# ---------------------------------------------------------------- F03/F02 session states
@REG
def test_tc_bb_037(client):
    for name in ("index", "dashboard"):
        r = S.page(client, name)
        assert r.status_code in (302, 303) and C.ROUTES["login"] in r.headers["Location"]


def test_tc_bb_038(user1):
    S.web_logout(user1)
    r = S.page(user1)
    assert r.status_code in (302, 303) and C.ROUTES["login"] in r.headers["Location"]


# ---------------------------------------------------------------- F09 filter / search
@pytest.fixture
def seeded(user1):
    work, study = S.category_id(user1, "Work"), S.category_id(user1, "Study")
    S.create_task_id(user1, "Write report", category_id=work)
    S.create_task_id(user1, "Revise chapter", category_id=study)
    done = S.create_task_id(user1, "Paid bills")
    user1.put(S.api("task", id=done), json={C.K_DONE: True})
    S.create_task_id(user1, "Mum's birthday")
    return user1, "Work"


@REG
def test_tc_bb_039(seeded):
    c, work = seeded
    html = S.text(S.page(c, query={C.Q_CATEGORY: work}))
    assert "Write report" in html and "Revise chapter" not in html


def test_tc_bb_040(seeded):
    c, _ = seeded
    done = S.text(S.page(c, query={C.Q_STATUS: "done"}))
    assert "Paid bills" in done and "Write report" not in done
    still_open = S.text(S.page(c, query={C.Q_STATUS: "open"}))
    assert "Write report" in still_open and "Paid bills" not in still_open


def test_tc_bb_041(seeded):
    c, _ = seeded
    html = S.text(S.page(c, query={C.Q_SEARCH: "repo"}))
    assert "Write report" in html and "Revise chapter" not in html


def test_tc_bb_042(seeded):
    c, _ = seeded
    r = S.page(c, query={C.Q_SEARCH: "zzz"})
    assert r.status_code == 200 and "Write report" not in S.text(r)


def test_tc_bb_043(seeded):
    c, work = seeded
    html = S.text(S.page(c, query={C.Q_CATEGORY: work, C.Q_SEARCH: "report"}))
    assert "Write report" in html and "Revise chapter" not in html


def test_tc_bb_044(seeded):
    c, _ = seeded
    r = S.page(c, query={C.Q_SEARCH: "Mum's"})
    assert r.status_code == 200 and "birthday" in S.text(r)


# ---------------------------------------------------------------- F11 dashboard
@REG
def test_tc_bb_045(user1):
    S.create_task_id(user1, "Late", due=S.day(-1))
    S.create_task_id(user1, "Soon", due=S.day(1))
    S.create_task_id(user1, "Later", due=S.day(5))
    S.create_task_id(user1, "Someday")
    d = S.create_task_id(user1, "Done today")
    user1.put(S.api("task", id=d), json={C.K_DONE: True})
    counts = S.dashboard_counts_from_html(S.text(S.page(user1, "dashboard")))
    assert counts == {"total": 5, "open": 4, "overdue": 1, "due_soon": 1, "completed": 1}, counts


@REG
@pytest.mark.defect("DEF-001")
def test_tc_bb_046(user1):
    S.create_task_id(user1, "Due today", due=S.day(0))
    counts = S.dashboard_counts_from_html(S.text(S.page(user1, "dashboard")))
    assert counts["overdue"] == 0, f"DEF-001: Overdue = {counts['overdue']} for a task due today"


# ---------------------------------------------------------------- F06 edit
def test_tc_bb_047(user1):
    tid = S.create_task_id(user1, "Original")
    study = S.category_id(user1, "Study")
    user1.post(S.route("edit_task", id=tid),
               data={C.F_TITLE: "Edited", C.F_CATEGORY: study, C.F_DUE: S.day(5)})
    t = task_json(user1, tid).get_json()
    assert t[C.K_TITLE] == "Edited" and t[C.K_DUE] == S.day(5) and t[C.K_CAT_ID] == study
    assert not t[C.K_DONE]


@pytest.mark.defect("DEF-009")
def test_tc_bb_048(user1):
    tid = S.create_task_id(user1, "Keep me")
    user1.post(S.route("edit_task", id=tid), data={C.F_TITLE: "   ", C.F_CATEGORY: "", C.F_DUE: ""})
    t = task_json(user1, tid).get_json()
    assert t[C.K_TITLE] == "Keep me", f"DEF-009: title changed to {t[C.K_TITLE]!r}"


@REG
@pytest.mark.defect("DEF-008")
def test_tc_bb_049(user1):
    S.web_new_task(user1, "Bad date", "", "2026-13-45")
    r = S.page(user1)
    assert r.status_code == 200, f"DEF-008: My Tasks returns HTTP {r.status_code} after invalid date"
    assert "Bad date" not in S.text(r)
