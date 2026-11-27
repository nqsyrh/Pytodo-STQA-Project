"""
Week 4 - REST API tests (46) with the Flask test client.

Request data for every case: 04_Web_API/api_request_data.json
Expected vs actual:          04_Web_API/PyTodo QA Data Collection (Week 4).xlsx
Rule: a 5xx answer to client input is always a failure - the server must answer 4xx.
"""
import pytest

import qa_config as C
import qa_support as S

pytestmark = pytest.mark.api
REG = pytest.mark.regression


def no_5xx(r):
    assert not S.is_server_error(r), f"server error HTTP {r.status_code} on client input"


# ----------------------------------------------------------------- POST /api/register
@REG
def test_tc_api_001(client):
    r = S.api_register(client, "api_ok")
    assert r.status_code == 201
    body = r.get_json()
    assert body["username"] == "api_ok" and "id" in body and "password" not in body


def test_tc_api_002(client):
    assert S.api_register(client, "ab").status_code == 400


def test_tc_api_003(client):
    assert S.api_register(client, "api_pw", "short").status_code == 400


def test_tc_api_004(client):
    assert client.post(S.api("register"), json={}).status_code == 400


@REG
@pytest.mark.defect("DEF-004")
def test_tc_api_005(client):
    S.api_register(client, "api_dup")
    r = S.api_register(client, "api_dup", "OtherPass9")
    assert r.status_code in (400, 409), f"DEF-004: duplicate accepted, HTTP {r.status_code} {r.get_json()}"


@pytest.mark.defect("DEF-018")
def test_tc_api_006(client):
    r = client.post(S.api("register"), json={"username": 12345, "password": C.PASSWORD})
    no_5xx(r)
    assert r.status_code == 400


# ----------------------------------------------------------------- POST /api/login
@REG
def test_tc_api_007(client):
    S.api_register(client, C.USER1)
    assert S.api_login(client, C.USER1).status_code == 200


def test_tc_api_008(client):
    S.api_register(client, C.USER1)
    assert S.api_login(client, C.USER1, "WrongPass1").status_code == 401


def test_tc_api_009(client):
    assert S.api_login(client, "ghost").status_code == 401


def test_tc_api_010(client):
    assert S.api_tasks(client).status_code == 401


# ----------------------------------------------------------------- GET /api/categories
@pytest.mark.defect("DEF-016")
def test_tc_api_011(client):
    r = client.get(S.api("categories"))
    assert r.status_code == 401, f"DEF-016: categories returned HTTP {r.status_code} without login"


def test_tc_api_012(user1):
    r = user1.get(S.api("categories"))
    assert r.status_code == 200
    assert sorted(c["name"] for c in r.get_json()) == sorted(C.CATEGORIES)


# ----------------------------------------------------------------- POST /api/tasks
@REG
def test_tc_api_013(user1):
    r = S.api_create(user1, "API task", category_id=1, due=S.day(3))
    assert r.status_code == 201
    t = r.get_json()
    assert t[C.K_TITLE] == "API task" and t[C.K_CAT_ID] == 1 and t[C.K_DUE] == S.day(3)


def test_tc_api_014(user1):
    r = S.api_create(user1, "Only title")
    assert r.status_code == 201 and r.get_json()[C.K_DUE] in (None, "")


def test_tc_api_015(user1):
    r = user1.post(S.api("tasks"), json={C.K_CAT_ID: 1})
    assert r.status_code == 400


@pytest.mark.defect("DEF-018")
def test_tc_api_016(user1):
    r = user1.post(S.api("tasks"), json={C.K_TITLE: 123})
    no_5xx(r)
    assert r.status_code == 400 or (r.status_code == 201 and r.get_json()[C.K_TITLE] == "123")


@REG
@pytest.mark.defect("DEF-008")
def test_tc_api_017(user1):
    r = S.api_create(user1, "x", due="2026-13-45")
    no_5xx(r)
    assert r.status_code == 400
    assert S.api_tasks(user1).status_code == 200


@pytest.mark.defect("DEF-008")
def test_tc_api_018(user1):
    r = S.api_create(user1, "x", due="21/11/2026")
    no_5xx(r)
    assert r.status_code == 400


@pytest.mark.defect("DEF-011")
def test_tc_api_019(user1):
    r = S.api_create(user1, "x", category_id=999)
    assert r.status_code == 400, f"DEF-011: unknown category accepted, HTTP {r.status_code}"


@pytest.mark.defect("DEF-017")
def test_tc_api_020(user1):
    r = user1.post(S.api("tasks"), data="hello", content_type="text/plain")
    assert r.status_code in (400, 415)
    assert "json" in (r.get_data(as_text=True)).lower(), "DEF-017: error does not mention JSON"


@pytest.mark.defect("DEF-013")
def test_tc_api_021(user1):
    r = S.api_create(user1, "a" * 5000)
    assert r.status_code == 400, f"DEF-013: 5,000-character title accepted (HTTP {r.status_code})"


# ----------------------------------------------------------------- GET /api/tasks/{id}
def test_tc_api_022(user1):
    tid = S.create_task_id(user1, "Mine")
    r = user1.get(S.api("task", id=tid))
    assert r.status_code == 200 and r.get_json()[C.K_ID] == tid


def test_tc_api_023(user1):
    assert user1.get(S.api("task", id=99999)).status_code == 404


@REG
def test_tc_api_024(user1, user2):
    other = S.create_task_id(user2, "qa_user2 private")
    assert user1.get(S.api("task", id=other)).status_code == 404


# ----------------------------------------------------------------- GET /api/tasks (list)
def titles(r):
    return [t[C.K_TITLE] for t in r.get_json()]


def test_tc_api_025(user1):
    for n in ("first", "second", "third"):
        S.create_task_id(user1, n)
    r = S.api_tasks(user1)
    assert r.status_code == 200 and titles(r)[:3] == ["third", "second", "first"]


def test_tc_api_026(user1):
    for n in range(5):
        S.create_task_id(user1, f"t{n}")
    r = S.api_tasks(user1, page=0, per_page=2)
    assert r.status_code == 200 and len(r.get_json()) == 2


@pytest.mark.defect("DEF-012")
def test_tc_api_027(user1):
    S.create_task_id(user1, "t")
    assert S.api_tasks(user1, page=-1).status_code == 400


@pytest.mark.defect("DEF-012")
def test_tc_api_028(user1):
    S.create_task_id(user1, "t")
    assert S.api_tasks(user1, per_page=0).status_code == 400


def test_tc_api_029(user1):
    S.create_task_id(user1, "t")
    r = S.api_tasks(user1, page=50)
    assert r.status_code == 200 and r.get_json() == []


def test_tc_api_030(user1):
    S.create_task_id(user1, "work one", category_id=1)
    S.create_task_id(user1, "study one", category_id=3)
    r = S.api_tasks(user1, **{C.Q_CATEGORY: "Work"})
    assert titles(r) == ["work one"]


def test_tc_api_031(user1):
    S.create_task_id(user1, "open one")
    d = S.create_task_id(user1, "done one")
    user1.put(S.api("task", id=d), json={C.K_DONE: True})
    r = S.api_tasks(user1, **{C.Q_STATUS: "done"})
    assert titles(r) == ["done one"]


def test_tc_api_032(user1):
    S.create_task_id(user1, "Write report")
    S.create_task_id(user1, "Revise chapter")
    assert titles(S.api_tasks(user1, **{C.Q_SEARCH: "repo"})) == ["Write report"]


@REG
@pytest.mark.defect("DEF-006")
def test_tc_api_033(user1):
    S.create_task_id(user1, "Mum's birthday")
    r = S.api_tasks(user1, **{C.Q_SEARCH: "Mum's"})
    no_5xx(r)
    assert titles(r) == ["Mum's birthday"]


# ----------------------------------------------------------------- PUT /api/tasks/{id}
def test_tc_api_034(user1):
    tid = S.create_task_id(user1, "Before", due=S.day(2))
    r = user1.put(S.api("task", id=tid), json={C.K_TITLE: "Renamed"})
    t = r.get_json()
    assert r.status_code == 200 and t[C.K_TITLE] == "Renamed" and t[C.K_DUE] == S.day(2)


@REG
@pytest.mark.defect("DEF-009")
def test_tc_api_035(user1):
    tid = S.create_task_id(user1, "Keep")
    r = user1.put(S.api("task", id=tid), json={C.K_TITLE: ""})
    assert r.status_code == 400
    assert user1.get(S.api("task", id=tid)).get_json()[C.K_TITLE] == "Keep"


@REG
@pytest.mark.defect("DEF-010")
def test_tc_api_036(user1):
    tid = S.create_task_id(user1, "Stay open")
    r = user1.put(S.api("task", id=tid), json={C.K_DONE: "false"})
    done = user1.get(S.api("task", id=tid)).get_json()[C.K_DONE]
    assert r.status_code == 400 or not done, "DEF-010: string 'false' marked the task as done"


def test_tc_api_037(user1, user2):
    other = S.create_task_id(user2, "qa_user2 task")
    r = user1.put(S.api("task", id=other), json={C.K_TITLE: "hacked"})
    assert r.status_code in (403, 404)
    assert user2.get(S.api("task", id=other)).get_json()[C.K_TITLE] == "qa_user2 task"


def test_tc_api_038(user1):
    assert user1.put(S.api("task", id=99999), json={C.K_TITLE: "x"}).status_code == 404


@pytest.mark.defect("DEF-008")
def test_tc_api_039(user1):
    tid = S.create_task_id(user1, "Date edit")
    r = user1.put(S.api("task", id=tid), json={C.K_DUE: "2026-13-45"})
    no_5xx(r)
    assert r.status_code == 400
    assert user1.get(S.api("task", id=tid)).status_code == 200


# ----------------------------------------------------------------- DELETE /api/tasks/{id}
@REG
def test_tc_api_040(user1):
    tid = S.create_task_id(user1, "Bye")
    assert user1.delete(S.api("task", id=tid)).status_code == 200
    assert user1.get(S.api("task", id=tid)).status_code == 404


@pytest.mark.defect("DEF-005")
def test_tc_api_041(user1):
    r = user1.delete(S.api("task", id=99999))
    assert r.status_code == 404, f"DEF-005: unknown id gave HTTP {r.status_code} {r.get_json()}"


@REG
@pytest.mark.defect("DEF-005")
def test_tc_api_042(user1, user2):
    other = S.create_task_id(user2, "qa_user2 keep")
    r = user1.delete(S.api("task", id=other))
    still_there = user2.get(S.api("task", id=other)).status_code == 200
    assert r.status_code in (403, 404) and still_there, "DEF-005: qa_user1 deleted qa_user2's task"


@REG
def test_tc_api_043(client):
    assert client.delete(S.api("task", id=1)).status_code == 401


# ----------------------------------------------------------------- GET /api/dashboard
def dash(c):
    d = c.get(S.api("dashboard")).get_json()
    return {k: d[v] for k, v in C.DASH_KEYS.items()}


def test_tc_api_044(user1):
    S.create_task_id(user1, "Late", due=S.day(-1))
    S.create_task_id(user1, "Soon", due=S.day(2))
    S.create_task_id(user1, "Later", due=S.day(6))
    d = S.create_task_id(user1, "Done")
    user1.put(S.api("task", id=d), json={C.K_DONE: True})
    assert dash(user1) == {"total": 4, "open": 3, "overdue": 1, "due_soon": 1, "completed": 1}


@REG
@pytest.mark.defect("DEF-001")
def test_tc_api_045(user1):
    S.create_task_id(user1, "Today", due=S.day(0))
    d = dash(user1)
    assert d["overdue"] == 0, f"DEF-001: {d}"


def test_tc_api_046(client):
    assert client.get(S.api("dashboard")).status_code == 401
