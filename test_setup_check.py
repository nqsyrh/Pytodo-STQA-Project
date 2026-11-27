"""
Run this FIRST after copying PyTodo Pro into ./app :
    pytest test_setup_check.py -v
It checks that qa_config.py matches your copy of the app (routes, JSON keys,
helper functions, dashboard labels). Fix any failure in qa_config.py only.
"""
import pytest

import qa_config as C
import qa_support as S


def test_app_imports_with_temp_db(app):
    assert app.test_client() is not None


def test_helpers_functions_exist():
    h = S.helpers()
    for fn in ("compute_urgency", "is_valid_password", "is_valid_username", "completed_in_last_n_days"):
        assert hasattr(h, fn), f"helpers.py has no {fn} - update the adapter in qa_support.py"


@pytest.mark.parametrize("name", [k for k in C.ROUTES if "{id}" not in C.ROUTES[k]])
def test_web_route_exists(user1, name):
    r = user1.get(S.route(name))
    assert r.status_code != 404, f"ROUTES['{name}'] = {C.ROUTES[name]} not found - fix qa_config.ROUTES"


def test_task_routes_and_json_keys(user1):
    tid = S.create_task_id(user1, "config check", category_id=1, due=S.day(1))
    t = user1.get(S.api("task", id=tid)).get_json()
    for k in (C.K_ID, C.K_TITLE, C.K_DONE, C.K_DUE, C.K_CAT_ID, C.K_COMPLETED_AT):
        assert k in t, f"JSON key {k!r} missing in {sorted(t)} - fix qa_config K_* names"
    for name in ("edit_task",):
        assert user1.get(S.route(name, id=tid)).status_code != 404, f"ROUTES['{name}'] wrong"
    r = user1.post(S.route("toggle_task", id=tid))
    assert r.status_code != 404 and r.status_code != 405, "ROUTES['toggle_task'] wrong (or not POST)"


def test_dashboard_labels_parse(user1):
    S.create_task_id(user1, "dash check", due=S.day(-1))
    counts = S.dashboard_counts_from_html(S.text(S.page(user1, "dashboard")))
    assert None not in counts.values(), f"could not read {counts} - fix DASH_LABELS / DASH_NUMBER_POSITION"
    api = user1.get(S.api("dashboard")).get_json()
    for k, v in C.DASH_KEYS.items():
        assert v in api, f"API dashboard key {v!r} missing in {sorted(api)}"
