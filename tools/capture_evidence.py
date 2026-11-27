"""
Capture screenshot evidence from the REAL app without a live server:
pages are rendered by the Flask test client (fresh temp DB), CSS is inlined,
and headless Chrome screenshots them at desktop / tablet / phone sizes.

    python tools/capture_evidence.py          (needs google-chrome or chromium)

Output: 03_Special_Testing/week 3 evidence/*.png and 05_Security_Performance/week 5 evidence/*.png
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import qa_config as C  # noqa: E402
import qa_support as S  # noqa: E402

CHROME = next((c for c in ("google-chrome", "chromium", "chromium-browser") if shutil.which(c)), None)
SIZES = {"desktop": (1366, 768), "tablet": (768, 1024), "phone": (375, 812)}
CSS = open(os.path.join(C.APP_DIR, "static", "style.css"), encoding="utf-8").read()
SHOTS = os.path.join(ROOT, "03_Special_Testing", "week 3 evidence")
SEC = os.path.join(ROOT, "05_Security_Performance", "week 5 evidence")
os.makedirs(SHOTS, exist_ok=True)
os.makedirs(SEC, exist_ok=True)
tmp = tempfile.mkdtemp()


def shoot(html, out, size=(1366, 768)):
    html = html.replace('<link rel="stylesheet" href="/static/style.css">', f"<style>{CSS}</style>")
    page = os.path.join(tmp, "page.html")
    open(page, "w", encoding="utf-8").write(html)
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={size[0]},{size[1]}", f"--screenshot={out}", "file://" + page],
                   check=True, capture_output=True)
    print("saved", os.path.relpath(out, ROOT))


app, mod = S.load_app(os.path.join(tmp, "evidence.db"))
anon = app.test_client()
user = app.test_client()
S.signup(user, C.USER1)
S.create_task_id(user, "Submit STQA report", category_id=1, due=S.day(0))      # DEF-001
S.create_task_id(user, "Revise chapter 5", category_id=3, due=S.day(1))
S.create_task_id(user, "Group meeting", category_id=2, due=S.day(4))
S.create_task_id(user, "Pay hostel fee", due=S.day(-1))
S.create_task_id(user, "Buy milk & eggs <b>bold?</b>")                          # DEF-007
done = S.create_task_id(user, "Read lecture notes", category_id=3)
user.put(S.api("task", id=done), json={C.K_DONE: True})

pages = {"login": (anon, "login"), "register": (anon, "register"), "my_tasks": (user, "index"),
         "new_task": (user, "new_task"), "dashboard": (user, "dashboard")}
for name, (client, route) in pages.items():
    html = S.text(client.get(S.route(route)))
    for size_name, size in SIZES.items():
        shoot(html, os.path.join(SHOTS, f"{name}_{size_name}.png"), size)
shoot(S.text(user.get(S.route("edit_task", id=done))), os.path.join(SHOTS, "edit_task_desktop.png"))
r = anon.post(S.route("register"), data={C.F_USERNAME: "eightchr", C.F_PASSWORD: "Abcd123!"})
shoot(S.text(r), os.path.join(SHOTS, "register_8char_password_DEF-002.png"), (900, 600))

# TC-SEC-013: Werkzeug debugger shown on a server error when debug is on (as supplied)
from werkzeug.debug import DebuggedApplication  # noqa: E402
from werkzeug.test import Client  # noqa: E402
user.post(S.api("tasks"), json={C.K_TITLE: "bad date", C.K_DUE: "2026-13-45"})
cookie = user.get_cookie(C.SESSION_COOKIE).value
app.config["PROPAGATE_EXCEPTIONS"] = True    # behave like python app.py (debug=True)
dbg = Client(DebuggedApplication(app, evalex=True))
dbg.set_cookie(C.SESSION_COOKIE, cookie)
resp = dbg.get("/")
shoot(resp.get_data(as_text=True), os.path.join(SEC, "werkzeug_debugger_TC-SEC-013.png"), (1366, 900))
print("HTTP", resp.status_code, "on / after invalid date (DEF-008)")
