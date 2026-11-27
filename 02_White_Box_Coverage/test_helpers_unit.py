"""
Week 2 - White-box unit tests (29).

Units (selection justified in White_Box_Analysis.md):
  helpers.compute_urgency          V(G)=5   TC-WB-001..008
  helpers.is_valid_password        V(G)=3   TC-WB-009..012
  helpers.is_valid_username        V(G)=4   TC-WB-013..018
  helpers.completed_in_last_n_days V(G)=4   TC-WB-019..025
  app.api_update_task (completed_at if/elif/else)  TC-WB-026..029

Coverage:  pytest 02_White_Box_Coverage --cov=app --cov=helpers --cov-branch \
           --cov-report=html:02_White_Box_Coverage/coverage_html
"""
from datetime import date, datetime, timedelta

import pytest

import qa_config as C
import qa_support as S

pytestmark = pytest.mark.unit
REG = pytest.mark.regression
TODAY = date(2026, 11, 21)                 # fixed reference date for basis paths
NOW = datetime(2026, 11, 21, 12, 0, 0)


# ------------------------------------------------------------ compute_urgency
@REG
def test_tc_wb_001():
    """Path 1-3-4-10: no due date."""
    assert S.compute_urgency(None, TODAY) == C.L_NONE


def test_tc_wb_002():
    """Path 1-2-3-5-7-9-10: today defaulted to date.today()."""
    far = (date.today() + timedelta(days=30)).isoformat()
    assert S.compute_urgency(far) == C.L_UPCOMING


@REG
def test_tc_wb_003():
    """Path 1-3-5-6-10: past date."""
    assert S.compute_urgency("2026-11-20", TODAY) == C.L_OVERDUE


@REG
@pytest.mark.defect("DEF-001")
def test_tc_wb_004():
    """Boundary of 'due <= today': due today must be 'Due Today'."""
    got = S.compute_urgency("2026-11-21", TODAY)
    assert got == C.L_TODAY, f"DEF-001: compute_urgency returned {got!r} for a task due today"


@REG
def test_tc_wb_005():
    """Path 1-3-5-7-8-10: 1 day away."""
    assert S.compute_urgency("2026-11-22", TODAY) == C.L_SOON


def test_tc_wb_006():
    """Upper edge of Due Soon (2 days)."""
    assert S.compute_urgency("2026-11-23", TODAY) == C.L_SOON


@REG
def test_tc_wb_007():
    """Path 1-3-5-7-9-10: 3 days away."""
    assert S.compute_urgency("2026-11-24", TODAY) == C.L_UPCOMING


def test_tc_wb_008():
    """Data-flow: an invalid stored date reaches strptime unchecked (root cause of DEF-008)."""
    with pytest.raises(ValueError):
        S.compute_urgency("2026-13-45", TODAY)


# ------------------------------------------------------------ is_valid_password
def test_tc_wb_009():
    assert S.is_valid_password("Abc123!") is False


@REG
@pytest.mark.defect("DEF-002")
def test_tc_wb_010():
    assert S.is_valid_password("Abcd123!") is True, "DEF-002: 8 characters rejected (len > 8)"


def test_tc_wb_011():
    assert S.is_valid_password("Abcd1234!") is True


def test_tc_wb_012():
    """Branch: empty string and non-string (None) are both invalid."""
    assert S.is_valid_password("") is False
    assert S.is_valid_password(None) is False


# ------------------------------------------------------------ is_valid_username
def test_tc_wb_013():
    """Branch: too short, and non-string (None) input."""
    assert S.is_valid_username("ab") is False
    assert S.is_valid_username(None) is False


def test_tc_wb_014():
    assert S.is_valid_username("abc") is True


def test_tc_wb_015():
    assert S.is_valid_username("u" * 20) is True


def test_tc_wb_016():
    assert S.is_valid_username("u" * 21) is False


def test_tc_wb_017():
    assert S.is_valid_username("qa-user") is False


def test_tc_wb_018():
    assert S.is_valid_username("qa_user1") is True


# ------------------------------------------------------------ completed_in_last_n_days
def test_tc_wb_019():
    assert S.completed_in_last_n_days(None, 7, NOW) is False


def test_tc_wb_020():
    assert S.completed_in_last_n_days(NOW - timedelta(days=3), 7, NOW) is True


@REG
@pytest.mark.defect("DEF-003")
def test_tc_wb_021():
    """Inclusive window: exactly 7 days ago still counts."""
    assert S.completed_in_last_n_days(NOW - timedelta(days=7), 7, NOW) is True, \
        "DEF-003: task completed exactly 7 days ago not counted (age.days < n)"


def test_tc_wb_022():
    assert S.completed_in_last_n_days(NOW - timedelta(days=8), 7, NOW) is False


def test_tc_wb_023():
    """Compound condition: age > 0 false (completed in the future)."""
    assert S.completed_in_last_n_days(NOW + timedelta(days=1), 7, NOW) is False


def test_tc_wb_024():
    assert S.completed_in_last_n_days(NOW - timedelta(days=6), 7, NOW) is True


def test_tc_wb_025():
    assert S.completed_in_last_n_days(NOW - timedelta(hours=2), 1, NOW) is True


# ------------------------------------------------------------ app.api_update_task (completed_at)
def get(c, tid):
    return c.get(S.api("task", id=tid)).get_json()


def test_tc_wb_026(user1):
    tid = S.create_task_id(user1, "wb open")
    user1.put(S.api("task", id=tid), json={C.K_DONE: True})
    assert get(user1, tid)[C.K_COMPLETED_AT]


def test_tc_wb_027(user1):
    tid = S.create_task_id(user1, "wb done")
    user1.put(S.api("task", id=tid), json={C.K_DONE: True})
    user1.put(S.api("task", id=tid), json={C.K_DONE: False})
    assert not get(user1, tid)[C.K_COMPLETED_AT]


def test_tc_wb_028(user1):
    tid = S.create_task_id(user1, "wb keep")
    user1.put(S.api("task", id=tid), json={C.K_DONE: True})
    before = get(user1, tid)[C.K_COMPLETED_AT]
    user1.put(S.api("task", id=tid), json={C.K_TITLE: "wb keep renamed"})
    assert get(user1, tid)[C.K_COMPLETED_AT] == before


def test_tc_wb_029(user1):
    tid = S.create_task_id(user1, "wb twice")
    user1.put(S.api("task", id=tid), json={C.K_DONE: True})
    user1.put(S.api("task", id=tid), json={C.K_DONE: True})
    t = get(user1, tid)
    assert t[C.K_DONE] and t[C.K_COMPLETED_AT]
