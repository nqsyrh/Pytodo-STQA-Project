"""
Build screenshot evidence for every automated test, from a run on the REAL app.

    QA_EVIDENCE=1 pytest -m "not ui"            # records every request/response
    python tools/capture_week_evidence.py      # renders + screenshots (needs Chrome)

For each test it renders one evidence card: test ID, PASS/FAIL, objective,
expected (written before execution), observed result, the test code, every
HTTP request/response the test made, and the last page the app rendered.
Cards are saved as PNG into the matching week folder:

    01_Black_Box/week 1 evidence/TC-BB-xxx.png
    02_White_Box_Coverage/week 2 evidence/TC-WB-xxx.png
    04_Web_API/week 4 evidence/TC-API-xxx.png
    05_Security_Performance/week 5 evidence/TC-SEC-xxx.png
plus run-log screenshots for weeks 2, 6 and 7.
"""
import ast
import glob
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import qa_config as C  # noqa: E402
import test_catalogue as T  # noqa: E402

CHROME = next((c for c in ("google-chrome", "chromium", "chromium-browser") if shutil.which(c)), None)
CSS = open(os.path.join(C.APP_DIR, "static", "style.css"), encoding="utf-8").read()
EVID = json.load(open(os.path.join(ROOT, "reports", "evidence.json"), encoding="utf-8"))
ENV = open(os.path.join(ROOT, "07_Test_Management", "Execution_Evidence", "environment.txt"), encoding="utf-8").read()
CASES = {c["Test Case ID"]: c for c in T.TEST_CASES}
FOLDERS = {"BB": "01_Black_Box/week 1 evidence", "WB": "02_White_Box_Coverage/week 2 evidence",
           "API": "04_Web_API/week 4 evidence", "SEC": "05_Security_Performance/week 5 evidence"}
SCRIPTS = {"BB": "01_Black_Box/test_black_box.py", "WB": "02_White_Box_Coverage/test_helpers_unit.py",
           "API": "04_Web_API/test_api.py", "SEC": "05_Security_Performance/test_security.py"}
TMP = tempfile.mkdtemp()
RUN = ENV.splitlines()[0].replace("Run date: ", "")


def sources():
    out = {}
    for path in SCRIPTS.values():
        src = open(os.path.join(ROOT, path), encoding="utf-8").read()
        lines = src.splitlines()
        for node in ast.parse(src).body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                start = min([d.lineno for d in node.decorator_list] + [node.lineno])
                out[node.name] = "\n".join(lines[start - 1:node.end_lineno])
    return out


SRC = sources()

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
body{{font-family:Arial,Helvetica,sans-serif;margin:0;background:#f3f5f8;color:#1d1d1f;font-size:13px}}
.wrap{{width:1220px;margin:0 auto;padding:18px}}
.head{{display:flex;justify-content:space-between;align-items:center;background:#1B3A5C;color:#fff;padding:12px 16px;border-radius:8px 8px 0 0}}
.head h1{{font-size:20px;margin:0}} .sub{{color:#cfe2f7;font-size:12px}}
.badge{{font-weight:700;padding:6px 14px;border-radius:16px;font-size:15px}}
.Pass{{background:#d8f3dc;color:#1e6b34}} .Fail{{background:#fdecea;color:#b3261e}}
.card{{background:#fff;border:1px solid #d9dee5;border-top:0;padding:12px 16px;border-radius:0 0 8px 8px}}
table{{border-collapse:collapse;width:100%}} td{{border:1px solid #e1e5ea;padding:5px 8px;vertical-align:top}}
td.k{{width:150px;background:#f6f8fa;font-weight:700}}
h2{{font-size:14px;margin:14px 0 6px;color:#1B3A5C}}
pre{{background:#0f1720;color:#e6edf3;padding:10px;border-radius:6px;white-space:pre-wrap;font-size:11.5px;margin:0}}
.ex{{font-family:Consolas,monospace;font-size:12px;border-bottom:1px dashed #e1e5ea;padding:4px 0}}
.m{{font-weight:700;color:#2C6B8F}} .u{{color:#8a6d00}} .s2{{color:#1e6b34;font-weight:700}} .s4{{color:#a15c00;font-weight:700}} .s5{{color:#b3261e;font-weight:700}}
.body{{color:#555;margin-left:18px;word-break:break-all}}
iframe{{width:100%;height:420px;border:1px solid #d9dee5;border-radius:6px;background:#fff}}
.foot{{color:#777;font-size:11px;margin-top:8px}}
</style></head><body><div class="wrap">{content}</div></body></html>"""


def status_class(code):
    return "s2" if code < 300 else ("s4" if code < 500 else "s5")


def card(cid, rec):
    c = CASES[cid]
    fn = "test_" + cid.lower().replace("-", "_")
    status = rec["status"]
    observed = c["Actual Result"] if status == c["Status"] else (rec.get("detail") or "")
    if status == "Fail" and rec.get("detail"):
        observed += "<div class='foot'>Assertion: " + html.escape(rec["detail"].splitlines()[0][:300]) + "</div>"
    rows = [("Requirement", f"{c['Feature/Requirement']} – {T.FEATURES[c['Feature/Requirement']]}"),
            ("Technique", c["Technique/Test Type"]), ("Objective", c["Objective"]),
            ("Preconditions", c["Preconditions"]), ("Test data", c["Test Data"]),
            ("Expected (pre-written)", c["Expected Result"]), ("Actual (observed)", None),
            ("Defect", c["Defect ID"] or "–")]
    trs = "".join(f"<tr><td class='k'>{k}</td><td>{observed if v is None else html.escape(str(v))}</td></tr>"
                  for k, v in rows)
    ex_html = ""
    last_page = None
    for e in rec.get("exchanges", []):
        loc = f" → {html.escape(e['location'])}" if e["location"] else ""
        ex_html += (f"<div class='ex'><span class='u'>[{html.escape(e.get('user', ''))}]</span> "
                    f"<span class='m'>{e['method']}</span> {html.escape(e['url'])} "
                    f"<span class='{status_class(e['status'])}'>{e['status']}</span>{loc}")
        if e["body"]:
            ex_html += f"<div class='body'>request: {html.escape(e['body'][:300])}</div>"
        if "json" in e["type"]:
            ex_html += f"<div class='body'>response: {html.escape(e['text'][:400])}</div>"
        elif e["status"] >= 500:
            ex_html += "<div class='body'>response: 500 Internal Server Error</div>"
        ex_html += "</div>"
        if "html" in e["type"] and e["status"] == 200 and "<nav" in e["text"]:
            last_page = e
    if not ex_html:
        ex_html = "<div class='ex'>Pure unit test – calls helpers.py directly (no HTTP request).</div>"
    frame = ""
    if last_page:
        page = last_page["text"].replace('<link rel="stylesheet" href="/static/style.css">', f"<style>{CSS}</style>")
        frame = (f"<h2>Page rendered by the app ({html.escape(last_page['method'])} {html.escape(last_page['url'])})</h2>"
                 f"<iframe srcdoc=\"{html.escape(page, quote=True)}\"></iframe>")
    content = (f"<div class='head'><div><h1>{cid} · {html.escape(c['Objective'])}</h1>"
               f"<div class='sub'>PyTodo Pro QA · {html.escape(c['Phase'])} · run {RUN} · real app, fresh temp DB</div></div>"
               f"<span class='badge {status}'>{status.upper()}</span></div>"
               f"<div class='card'><table>{trs}</table>"
               f"<h2>HTTP exchanges with the app ({len(rec.get('exchanges', []))})</h2>{ex_html}{frame}"
               f"<h2>Automated test code ({SCRIPTS[cid.split('-')[1]]}::{fn})</h2>"
               f"<pre>{html.escape(SRC.get(fn, ''))}</pre>"
               f"<div class='foot'>Evidence generated by tools/capture_week_evidence.py from reports/evidence.json "
               f"(QA_EVIDENCE=1 pytest -m \"not ui\"). App SHA-256 in 07_Test_Management/Execution_Evidence/environment.txt.</div>"
               f"</div>")
    return PAGE.format(content=content)


def shoot(page_html, out, width=1260, height=2200):
    path = os.path.join(TMP, "card.html")
    open(path, "w", encoding="utf-8").write(page_html)
    raw = os.path.join(TMP, "raw.png")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={width},{height}", f"--screenshot={raw}", "file://" + path],
                   check=True, capture_output=True)
    from PIL import Image, ImageChops
    im = Image.open(raw).convert("RGB")
    bg = Image.new("RGB", im.size, (243, 245, 248))
    box = ImageChops.difference(im, bg).getbbox()
    if box:
        im = im.crop((0, 0, im.width, min(im.height, box[3] + 18)))
    im.save(out, optimize=True)


def terminal(title, text, out):
    content = (f"<div class='head'><div><h1>{html.escape(title)}</h1><div class='sub'>run {RUN} · real app</div></div></div>"
               f"<div class='card'><pre>{html.escape(text)}</pre></div>")
    shoot(PAGE.format(content=content), out)


def main():
    assert CHROME, "Chrome/Chromium not found"
    n = 0
    for cid, rec in sorted(EVID.items()):
        phase = cid.split("-")[1]
        folder = os.path.join(ROOT, FOLDERS[phase])
        os.makedirs(folder, exist_ok=True)
        shoot(card(cid, rec), os.path.join(folder, f"{cid}_{rec['status'].upper()}.png"))
        n += 1
        if n % 20 == 0:
            print(n, "cards")
    ev = os.path.join(ROOT, "07_Test_Management", "Execution_Evidence")

    def tail(name, keep=80):
        lines = open(os.path.join(ev, name), encoding="utf-8").read().splitlines()
        return "\n".join(lines[-keep:])

    terminal("Week 2 – white-box unit tests (pytest -m unit)", tail("pytest_unit.log", 45),
             os.path.join(ROOT, FOLDERS["WB"], "run_pytest_unit.png"))
    terminal("Week 2 – statement coverage on the real app (python tools/statement_coverage.py)",
             open(os.path.join(ev, "statement_coverage.txt")).read() +
             "\n\nhelpers.py: every executable line ran.\napp.py: only 242, 266 (GET forms, Selenium only), "
             "375 (API status=open, gap) and 481-482 (start-up block) did not run.",
             os.path.join(ROOT, FOLDERS["WB"], "run_statement_coverage.png"))
    os.makedirs(os.path.join(ROOT, "06_Automation_Regression", "week 6 evidence"), exist_ok=True)
    terminal("Week 6 – focused regression suite (pytest -m \"regression and not ui\")", tail("pytest_regression.log", 60),
             os.path.join(ROOT, "06_Automation_Regression", "week 6 evidence", "run_regression_suite.png"))
    terminal("Week 7 – full automated run, summary (pytest -m \"not ui\")", ENV + "\n" + tail("pytest_all.log", 45),
             os.path.join(ev, "run_full_suite_summary.png"))
    print(n, "cards + 4 run screenshots written")


if __name__ == "__main__":
    main()
