"""Run axe-core (WCAG 2.1 A + AA rules) on every page and save JSON results.

Get axe once:  npm install axe-core   (then copy node_modules/axe-core/axe.min.js here)
App must be running at BASE_URL.  Usage: python axe_scan.py"""
import json
import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import qa_config as C  # noqa: E402
from selenium import webdriver  # noqa: E402
from selenium.webdriver.common.by import By  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
AXE = open(os.path.join(HERE, "axe.min.js"), encoding="utf-8").read()
OUT = os.path.join(HERE, "..", "axe_results")
os.makedirs(OUT, exist_ok=True)

opts = webdriver.ChromeOptions()
opts.add_argument("--headless=new")
d = webdriver.Chrome(options=opts)


def scan(name):
    d.execute_script(AXE)
    res = d.execute_async_script(
        "const cb = arguments[arguments.length-1];"
        "axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa']}})"
        ".then(r => cb(r));")
    with open(os.path.join(OUT, f"{name}.json"), "w") as fh:
        json.dump(res["violations"], fh, indent=2)
    for v in res["violations"]:
        print(f"{name:12} {v['impact']:9} {v['id']:22} {len(v['nodes'])} node(s)")


for page in ("login", "register"):
    d.get(C.BASE_URL + C.ROUTES[page])
    scan(page)
d.get(C.BASE_URL + C.ROUTES["register"])
d.find_element(By.NAME, C.F_USERNAME).send_keys("axe_" + uuid.uuid4().hex[:8])
d.find_element(By.NAME, C.F_PASSWORD).send_keys(C.PASSWORD)
d.find_element(By.CSS_SELECTOR, "form [type=submit]").click()
for page in ("index", "new_task", "dashboard"):
    d.get(C.BASE_URL + C.ROUTES[page])
    scan(page)
d.quit()
