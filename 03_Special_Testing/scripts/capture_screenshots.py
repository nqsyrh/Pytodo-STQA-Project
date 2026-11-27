"""Compatibility screenshots in a REAL browser against the LIVE app (TC-COMP-00x).

    set BROWSER=edge        (chrome | edge | firefox)
    python 03_Special_Testing/scripts/capture_screenshots.py

Start the app first (cd app && python app.py). Registers a throw-away user, adds
four tasks (overdue, due today, due soon, upcoming) and saves Login, Register,
My Tasks, New Task, Edit Task and Dashboard at desktop, tablet and phone size to
03_Special_Testing/week 3 evidence/<browser>/  plus a small layout check report.
Chrome/Edge use device emulation for exact viewports; Firefox uses window sizes.
"""
import json
import os
import sys
import uuid
from datetime import date, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import qa_config as C  # noqa: E402
from selenium import webdriver  # noqa: E402
from selenium.webdriver.common.by import By  # noqa: E402

NAME = C.BROWSER.lower()
OUT = os.path.join(os.path.dirname(__file__), "..", "week 3 evidence", NAME)
SIZES = {"desktop": (1366, 768), "tablet": (768, 1024), "phone": (375, 812)}
os.makedirs(OUT, exist_ok=True)

if NAME == "edge":
    d = webdriver.Edge()
elif NAME == "firefox":
    d = webdriver.Firefox()
else:
    d = webdriver.Chrome()
caps = d.capabilities
version = f"{caps.get('browserName')} {caps.get('browserVersion')} on {caps.get('platformName')}"
chromium = NAME in ("edge", "chrome")


def viewport(w, h):
    if chromium:
        d.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",
                          {"width": w, "height": h, "deviceScaleFactor": 1, "mobile": w < 500})
    else:
        d.set_window_size(w, h + 100)


def go(route, **kw):
    d.get(C.BASE_URL + C.ROUTES[route].format(**kw))


report = {"browser": version, "checks": {}}
user = "compat_" + uuid.uuid4().hex[:8]
d.set_window_size(1400, 900)
go("register")
d.find_element(By.NAME, C.F_USERNAME).send_keys(user)
d.find_element(By.NAME, C.F_PASSWORD).send_keys(C.PASSWORD)
d.find_element(By.CSS_SELECTOR, "form [type=submit]").click()
report["checks"]["register_and_login"] = "Pass" if d.current_url.rstrip("/").endswith("5000") else "Fail"
for off, title in ((-1, "Overdue sample"), (0, "Due today sample"), (2, "Due soon sample"), (5, "Upcoming sample")):
    go("new_task")
    d.find_element(By.NAME, C.F_TITLE).send_keys(title)
    d.execute_script("arguments[0].value=arguments[1]", d.find_element(By.NAME, C.F_DUE),
                     (date.today() + timedelta(days=off)).isoformat())
    d.find_element(By.CSS_SELECTOR, "form [type=submit]").click()
go("index")
report["checks"]["create_tasks"] = "Pass" if "Upcoming sample" in d.page_source else "Fail"
report["checks"]["due_today_badge"] = "Pass" if "Due Today" in d.page_source else "Fail (DEF-001: shows Overdue)"
first_task = d.find_element(By.CSS_SELECTOR, "a[href*='/edit']").get_attribute("href")

for size, (w, h) in SIZES.items():
    viewport(w, h)
    for page in ("index", "new_task", "dashboard"):
        go(page)
        d.save_screenshot(os.path.join(OUT, f"{page}_{size}.png"))
    d.get(first_task)
    d.save_screenshot(os.path.join(OUT, f"edit_task_{size}.png"))
    go("index")
    overflow = d.execute_script("return document.documentElement.scrollWidth > window.innerWidth;")
    report["checks"][f"no_sideways_scroll_{size}"] = "Pass" if not overflow else "Fail (DEF-023: sideways scroll)"

d.get(C.BASE_URL + C.ROUTES["logout"])
for size, (w, h) in SIZES.items():
    viewport(w, h)
    for page in ("login", "register"):
        go(page)
        d.save_screenshot(os.path.join(OUT, f"{page}_{size}.png"))
report["checks"]["logout_protects_pages"] = "Pass" if (go("index") or C.ROUTES["login"] in d.current_url) else "Fail"
d.quit()

with open(os.path.join(OUT, "compatibility_result.json"), "w") as fh:
    json.dump(report, fh, indent=2)
print(json.dumps(report, indent=2))
print("18 screenshots saved to", os.path.abspath(OUT))
