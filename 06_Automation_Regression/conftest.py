"""Selenium fixtures. Start the app first:  cd app && python app.py
Then:  pytest -m ui            (BROWSER=chrome|edge|firefox, HEADLESS=0 to watch)"""
import os
import uuid

import pytest

import qa_config as C

try:                                   # without Selenium installed, skip collection
    import selenium  # noqa: F401
except ImportError:
    collect_ignore = ["test_ui_selenium.py"]

SHOTS = os.path.join(os.path.dirname(__file__), "week 6 evidence", "selenium_screenshots")


@pytest.fixture
def driver(request):
    webdriver = pytest.importorskip("selenium.webdriver")
    name = C.BROWSER.lower()
    if name == "firefox":
        opts = webdriver.FirefoxOptions()
        if C.HEADLESS:
            opts.add_argument("-headless")
        drv = webdriver.Firefox(options=opts)
    elif name == "edge":
        opts = webdriver.EdgeOptions()
        if C.HEADLESS:
            opts.add_argument("--headless=new")
        drv = webdriver.Edge(options=opts)
    else:
        opts = webdriver.ChromeOptions()
        if C.HEADLESS:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1366,768")
        drv = webdriver.Chrome(options=opts)
    drv.implicitly_wait(2)
    caps = drv.capabilities
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "reports"), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "..", "reports", f"browser_{C.BROWSER}.txt"), "w") as fh:
        fh.write(f"{caps.get('browserName')} {caps.get('browserVersion')} on {caps.get('platformName')}\n")
    yield drv
    os.makedirs(SHOTS, exist_ok=True)
    drv.save_screenshot(os.path.join(SHOTS, f"{request.node.name}_{C.BROWSER}.png"))
    drv.quit()


@pytest.fixture
def new_user():
    return "ui_" + uuid.uuid4().hex[:10]
