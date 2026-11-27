"""
Week 6 - Selenium end-to-end tests AT-001..AT-010 (Page Object Model).

Each script is traced to the manual cases it automates
(Manual_to_Automated_Traceability.md).  Needs the app running at BASE_URL.
The 'smoke' subset is the compatibility smoke set for TC-COMP-002..004:
    BROWSER=edge pytest -m smoke
"""
from datetime import date, timedelta

import pytest
from selenium.webdriver.common.by import By

import qa_config as C
from pages.auth_pages import LoginPage, RegisterPage, logout
from pages.task_pages import DashboardPage, MyTasksPage, TaskFormPage

pytestmark = pytest.mark.ui
REG = pytest.mark.regression


def iso(offset):
    return (date.today() + timedelta(days=offset)).isoformat()


def signed_in(driver, user):
    RegisterPage(driver).register(user)
    return MyTasksPage(driver)


@REG
@pytest.mark.smoke
def test_at_001(driver, new_user):
    """TC-BB-002 / TC-BB-013: register and land on My Tasks."""
    page = RegisterPage(driver).register(new_user)
    assert page.path.rstrip("/") == C.ROUTES["index"].rstrip("/")


@REG
@pytest.mark.defect("DEF-002")
def test_at_002(driver, new_user):
    """TC-BB-010: 8-character password accepted."""
    page = RegisterPage(driver).register(new_user, "Abcd123!")
    assert page.path.rstrip("/") == C.ROUTES["index"].rstrip("/"), "DEF-002: " + page.message()


@REG
@pytest.mark.smoke
def test_at_003(driver, new_user):
    """TC-BB-017 / TC-BB-038: login, logout, protected page."""
    RegisterPage(driver).register(new_user)
    logout(driver)
    LoginPage(driver).login(new_user)
    assert LoginPage(driver).path.rstrip("/") == C.ROUTES["index"].rstrip("/")
    logout(driver)
    MyTasksPage(driver).open()
    assert C.ROUTES["login"] in driver.current_url


@REG
@pytest.mark.defect("DEF-001")
def test_at_004(driver, new_user):
    """TC-BB-026: a task due today shows the 'Due Today' badge."""
    tasks = signed_in(driver, new_user)
    TaskFormPage(driver).create("UI due today", due_iso=iso(0))
    row = tasks.open().row("UI due today")
    assert C.L_TODAY in row.text, f"DEF-001: badge shows {row.text!r}"


@pytest.mark.smoke
def test_at_005(driver, new_user):
    """TC-BB-032 / TC-BB-033: complete and reopen."""
    tasks = signed_in(driver, new_user)
    TaskFormPage(driver).create("UI toggle")
    tasks.open().toggle("UI toggle")
    assert C.L_DONE in tasks.open().row("UI toggle").text
    tasks.toggle("UI toggle")
    assert C.L_DONE not in tasks.open().row("UI toggle").text


def test_at_006(driver, new_user):
    """TC-BB-034 / TC-GUI-007: delete asks for confirmation."""
    tasks = signed_in(driver, new_user)
    TaskFormPage(driver).create("UI delete")
    tasks.open().delete("UI delete", accept=False)
    assert tasks.open().row("UI delete") is not None
    tasks.delete("UI delete", accept=True)
    assert tasks.open().row("UI delete") is None


@pytest.mark.smoke
def test_at_007(driver, new_user):
    """TC-BB-039: category filter."""
    tasks = signed_in(driver, new_user)
    TaskFormPage(driver).create("UI work", category="Work")
    TaskFormPage(driver).create("UI study", category="Study")
    tasks.open().filter_category("Work")
    body = tasks.page_text()
    assert "UI work" in body and "UI study" not in body


@pytest.mark.defect("DEF-007")
def test_at_008(driver, new_user):
    """TC-BB-024 / TC-SEC-012: HTML in a title is shown as text."""
    tasks = signed_in(driver, new_user)
    TaskFormPage(driver).create("<b>bold</b> UI")
    assert "<b>bold</b> UI" in tasks.open().page_text(), "DEF-007: title rendered as HTML"


@pytest.mark.smoke
def test_at_009(driver, new_user):
    """TC-BB-045: dashboard counters."""
    signed_in(driver, new_user)
    TaskFormPage(driver).create("UI late", due_iso=iso(-1))
    TaskFormPage(driver).create("UI soon", due_iso=iso(1))
    TaskFormPage(driver).create("UI someday")
    c = DashboardPage(driver).counters()
    assert (c["total"], c["open"], c["overdue"], c["due_soon"]) == (3, 3, 1, 1), c


def test_at_010(driver, new_user):
    """TC-GUI-006: the browser blocks an empty title (HTML5 required)."""
    signed_in(driver, new_user)
    form = TaskFormPage(driver).open()
    form.click(form.SAVE)
    assert form.path == C.ROUTES["new_task"]
    valid = driver.execute_script("return arguments[0].validity.valid;", form.find(form.TITLE))
    assert valid is False
