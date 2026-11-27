"""
Rebuild every test-management document from tools/test_catalogue.py
(and from reports/results.json when PyTest has been run).

    python tools/build_documents.py

Outputs: per-phase test-case workbooks, the master test-management workbook
(repository, RTM, defect log, risk register, execution status, metrics),
RTM.md, Defect_Reports.md, Regression_Suite.md and api_request_data.json.
"""
import json
import os
import re
import sys
from collections import Counter, OrderedDict
from datetime import date

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import test_catalogue as T  # noqa: E402

FONT = "Arial"
HEAD_FILL = PatternFill("solid", start_color="1F3864")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WIDTHS = {"Test Case ID": 12, "Feature/Requirement": 11, "Technique/Test Type": 24, "Objective": 34,
          "Preconditions": 24, "Test Data": 30, "Steps": 34, "Expected Result": 34, "Actual Result": 38,
          "Status": 9, "Evidence": 34, "Defect ID": 10, "Priority": 9, "Automated": 10, "Regression": 11,
          "Phase": 18}


# --------------------------------------------------------------------------- results merge
def merged_cases():
    cases = [OrderedDict(c) for c in T.TEST_CASES]
    path = os.path.join(ROOT, "reports", "results.json")
    if not os.path.exists(path):
        return add_evidence_paths(cases), []
    res = json.load(open(path, encoding="utf-8"))
    changed = []
    for c in cases:
        r = res.get(c["Test Case ID"])
        if r and r["status"] != c["Status"]:
            changed.append((c["Test Case ID"], c["Status"], r["status"]))
            c["Status"] = r["status"]
            c["Actual Result"] = (r.get("detail") or "As expected")[:300] + f" (re-run {date.today()})"
    return add_evidence_paths(cases), changed


WEEK_DIR = {"BB": "01_Black_Box/week 1 evidence", "WB": "02_White_Box_Coverage/week 2 evidence",
            "API": "04_Web_API/week 4 evidence", "SEC": "05_Security_Performance/week 5 evidence"}
GUI_SHOT = {"TC-GUI-008": "my_tasks_desktop.png", "TC-GUI-012": "my_tasks_desktop.png",
            "TC-GUI-013": "my_tasks_tablet.png", "TC-GUI-014": "my_tasks_phone.png",
            "TC-GUI-015": "register_8char_password_DEF-002.png", "TC-ACC-005": "my_tasks_desktop.png",
            "TC-ACC-010": "my_tasks_phone.png", "TC-ACC-011": "my_tasks_desktop.png",
            "TC-COMP-001": "my_tasks_desktop.png",
            "TC-COMP-002": "chrome/index_desktop.png",
            "TC-COMP-003": "edge/index_desktop.png", "TC-COMP-004": "firefox/index_desktop.png"}


def add_evidence_paths(cases):
    for c in cases:
        cid = c["Test Case ID"]
        ph = cid.split("-")[1] if cid.startswith("TC-") else "AT"
        if ph in WEEK_DIR and c["Automated"] == "Yes":
            shot = f"{WEEK_DIR[ph]}/{cid}_{c['Status'].upper()}.png"
            if os.path.exists(os.path.join(ROOT, shot)):
                c["Evidence"] = shot + "; log: 07_Test_Management/Execution_Evidence/pytest_all.log"
        elif cid in GUI_SHOT:
            c["Evidence"] = "03_Special_Testing/week 3 evidence/" + GUI_SHOT[cid]
        elif cid == "TC-SEC-013":
            c["Evidence"] = "05_Security_Performance/week 5 evidence/werkzeug_debugger_TC-SEC-013.png"
    return cases


# --------------------------------------------------------------------------- xlsx helpers
def style_header(ws, ncols, row=1):
    for col in range(1, ncols + 1):
        c = ws.cell(row=row, column=col)
        c.font = Font(name=FONT, bold=True, color="FFFFFF")
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = BORDER


def write_table(ws, headers, rows, widths=None, status_col=None):
    ws.append(headers)
    style_header(ws, len(headers))
    for r in rows:
        ws.append(list(r))
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(headers)):
        for c in row:
            c.font = Font(name=FONT, size=10)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = BORDER
    for i, h in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(h, WIDTHS.get(h, 18))
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{ws.max_row}"
    if status_col:
        col = get_column_letter(headers.index(status_col) + 1)
        rng = f"{col}2:{col}{ws.max_row}"
        for val, color in (("Pass", "C6EFCE"), ("Fail", "FFC7CE"), ("Not Run", "FFEB9C"), ("Blocked", "D9D9D9")):
            ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[f'"{val}"'],
                                                          fill=PatternFill("solid", start_color=color)))


def title_rows(ws, title, note):
    ws.insert_rows(1, 2)
    ws["A1"] = title
    ws["A1"].font = Font(name=FONT, bold=True, size=13)
    ws["A2"] = note
    ws["A2"].font = Font(name=FONT, italic=True, size=9, color="595959")
    ws.freeze_panes = "B4"
    ws.auto_filter.ref = ws.auto_filter.ref.replace("A1", "A3").replace(
        re.sub(r"\D", "", ws.auto_filter.ref.split(":")[1]), str(ws.max_row))


TEMPLATE = ["Test Case ID", "Feature/Requirement", "Technique/Test Type", "Objective", "Preconditions",
            "Test Data", "Steps", "Expected Result", "Actual Result", "Status", "Evidence", "Defect ID"]
MGMT = TEMPLATE + ["Priority", "Automated", "Regression", "Phase"]


def case_sheet(wb, name, cases, title):
    ws = wb.create_sheet(name)
    write_table(ws, TEMPLATE + ["Priority"], [[c[h] for h in TEMPLATE + ["Priority"]] for c in cases],
                status_col="Status")
    return ws


def phase_workbook(path, sheets):
    wb = Workbook()
    wb.remove(wb.active)
    for name, cases, title in sheets:
        case_sheet(wb, name, cases, title)
    wb.save(os.path.join(ROOT, path))


# --------------------------------------------------------------------------- master workbook
def master_workbook(cases):
    wb = Workbook()
    ws = wb.active
    ws.title = "Master Test Repository"
    write_table(ws, MGMT, [[c[h] for h in MGMT] for c in cases], status_col="Status")
    n = len(cases) + 1          # last data row
    rng = lambda col: f"'Master Test Repository'!${col}$2:${col}${n}"  # noqa: E731

    # ---- RTM (brief's RTM template columns)
    rtm = wb.create_sheet("RTM")
    rows = []
    for f, name in T.FEATURES.items():
        fc = [c for c in cases if c["Feature/Requirement"] == f]
        techs = sorted({tech_family(c["Technique/Test Type"]) for c in fc})
        ex = [c for c in fc if c["Status"] in ("Pass", "Fail")]
        defects = sorted({c["Defect ID"] for c in fc if c["Defect ID"]})
        rows.append([f"{f} {name}", T.SCENARIOS[f], compress_ids([c["Test Case ID"] for c in fc]),
                     ", ".join(techs), f"{sum(c['Status'] == 'Pass' for c in fc)}/{len(ex)} passed"
                     + (f" ({len(fc) - len(ex)} not run)" if len(fc) > len(ex) else ""), ", ".join(defects)])
    write_table(rtm, ["Requirement/Feature", "Test Scenario", "Test Case ID(s)", "Test Type/Technique",
                      "Result", "Defect ID"], rows,
                widths={"Requirement/Feature": 20, "Test Scenario": 40, "Test Case ID(s)": 40,
                        "Test Type/Technique": 40, "Result": 18, "Defect ID": 30})

    # ---- Defect log (Defect Report Template)
    dl = wb.create_sheet("Defect Log")
    dh = list(T.DEFECTS[0].keys())
    write_table(dl, dh, [[d[h] for h in dh] for d in T.DEFECTS],
                widths={"Defect ID": 10, "Title": 40, "Steps to Reproduce": 40, "Expected Result": 30,
                        "Actual Result": 36, "Environment": 26, "Evidence": 30, "Preconditions": 22})

    # ---- Risk register
    rr = wb.create_sheet("Risk Register")
    write_table(rr, ["ID", "Product risk", "Likelihood Wk 1", "Impact", "Score Wk 1", "Likelihood final",
                     "Score final", "Evidence"],
                [[r[0], r[1], r[2], r[3], None, r[4], None, r[5]] for r in T.RISKS],
                widths={"ID": 7, "Product risk": 40, "Evidence": 30})
    for i in range(2, len(T.RISKS) + 2):
        rr[f"E{i}"] = f"=C{i}*D{i}"
        rr[f"G{i}"] = f"=F{i}*D{i}"
    rr.cell(row=len(T.RISKS) + 3, column=1,
            value="Likelihood and impact 1-3 (team judgement); score = likelihood x impact.").font = Font(
        name=FONT, italic=True, size=9)

    # ---- Execution status (formulas over the master repository)
    es = wb.create_sheet("Execution Status")
    hdr = ["Phase", "Planned", "Executed", "Passed", "Failed", "Blocked", "Not Run", "Pass rate"]
    phases = [p[0] for p in T.PHASES.values()]
    write_table(es, hdr, [[p] for p in phases] + [["Total"]], widths={"Phase": 22})
    for i, _ in enumerate(phases, start=2):
        es[f"B{i}"] = f"=COUNTIF({rng('P')},A{i})"
        for col, st in (("D", "Pass"), ("E", "Fail"), ("F", "Blocked"), ("G", "Not Run")):
            es[f"{col}{i}"] = f'=COUNTIFS({rng("P")},$A{i},{rng("J")},"{st}")'
        es[f"C{i}"] = f"=D{i}+E{i}+F{i}"
        es[f"H{i}"] = f"=IF(C{i}=0,0,D{i}/C{i})"
    t = len(phases) + 2
    for col in "BCDEFG":
        es[f"{col}{t}"] = f"=SUM({col}2:{col}{t - 1})"
    es[f"H{t}"] = f"=IF(C{t}=0,0,D{t}/C{t})"
    for i in range(2, t + 1):
        es[f"H{i}"].number_format = "0.0%"
    for col in "ABCDEFGH":
        es[f"{col}{t}"].font = Font(name=FONT, bold=True, size=10)

    # ---- Metrics
    me = wb.create_sheet("Metrics")
    write_table(me, ["Metric", "Formula / working", "Value"], [], widths={"Metric": 34, "Formula / working": 44,
                                                                          "Value": 14})
    E = "'Execution Status'!"
    D = "'Defect Log'!"
    metrics = [
        ("Planned test cases", "count", f"={E}B{t}", "0"),
        ("Executed test cases", "passed + failed + blocked", f"={E}C{t}", "0"),
        ("Passed", "count", f"={E}D{t}", "0"),
        ("Failed", "count", f"={E}E{t}", "0"),
        ("Blocked", "count", f"={E}F{t}", "0"),
        ("Not run", "count", f"={E}G{t}", "0"),
        ("Execution rate", "executed / planned", f"={E}C{t}/{E}B{t}", "0.0%"),
        ("Pass rate", "passed / executed", f"={E}D{t}/{E}C{t}", "0.0%"),
        ("Automated test cases", "Automated = Yes", f'=COUNTIF({rng("N")},"Yes")', "0"),
        ("Automation rate", "automated / planned", "=C10/C2", "0.0%"),
        ("Regression suite size", "Regression = Yes", f'=COUNTIF({rng("O")},"Yes")', "0"),
        ("Regression passed", "Regression = Yes and Pass",
         f'=COUNTIFS({rng("O")},"Yes",{rng("J")},"Pass")', "0"),
        ("Confirmed defects", "count of defect log", f"=COUNTA({D}A2:A{len(T.DEFECTS) + 1})", "0"),
        ("Critical defects", "severity = Critical", f'=COUNTIF({D}J2:J{len(T.DEFECTS) + 1},"Critical")', "0"),
        ("Major defects", "severity = Major", f'=COUNTIF({D}J2:J{len(T.DEFECTS) + 1},"Major")', "0"),
        ("Moderate defects", "severity = Moderate", f'=COUNTIF({D}J2:J{len(T.DEFECTS) + 1},"Moderate")', "0"),
        ("Minor defects", "severity = Minor", f'=COUNTIF({D}J2:J{len(T.DEFECTS) + 1},"Minor")', "0"),
        ("Size of code under test (KLOC)", "app.py 482 + helpers.py 75 lines (input)", 0.557, "0.000"),
        ("Defect density (per KLOC)", "confirmed defects / KLOC", "=C14/C19", "0.0"),
        ("Failed tests linked to a defect", "failed with Defect ID / failed",
         f'=COUNTIFS({rng("J")},"Fail",{rng("L")},"<>")/C5', "0.0%"),
    ]
    for i, (m, w, f, fmt) in enumerate(metrics, start=2):
        me.cell(row=i, column=1, value=m)
        me.cell(row=i, column=2, value=w)
        c = me.cell(row=i, column=3, value=f)
        c.number_format = fmt
        for col in (1, 2, 3):
            me.cell(row=i, column=col).font = Font(name=FONT, size=10,
                                                   color="0000FF" if isinstance(f, float) else "000000")
            me.cell(row=i, column=col).border = BORDER
    me.cell(row=len(metrics) + 3, column=1,
            value="Blue = hardcoded input (line count of the supplied app). Everything else is a formula "
                  "over the Master Test Repository and Defect Log.").font = Font(name=FONT, italic=True, size=9)

    # ---- Read me
    rd = wb.create_sheet("Read Me", 0)
    lines = ["PyTodo Pro - Test Management Workbook (PYTODO-STP v2.0)",
             "Generated from tools/test_catalogue.py by tools/build_documents.py; statuses are updated from "
             "reports/results.json after each PyTest run.",
             "Master Test Repository: all test cases with the brief's Test Case Template fields + priority, "
             "automation and regression flags.",
             "RTM: brief's RTM template (requirement, scenario, test case IDs, technique, result, defect IDs).",
             "Defect Log: brief's Defect Report Template for all confirmed defects.",
             "Risk Register: Week 1 vs final likelihood (score formulas).",
             "Execution Status and Metrics: live formulas - change a Status in the repository and they update.",
             "Status values: Pass / Fail / Blocked / Not Run. Severity: Critical / Major / Moderate / Minor. "
             "Priority: High / Medium / Low."]
    for i, l in enumerate(lines, 1):
        rd.cell(row=i, column=1, value=l).font = Font(name=FONT, bold=(i == 1), size=13 if i == 1 else 10)
    rd.column_dimensions["A"].width = 120
    wb.save(os.path.join(ROOT, "07_Test_Management", "PyTodo_Test_Management.xlsx"))
    return rows


FAMILIES = [("Decision", "Decision table"), ("State", "State transition"), ("BVA", "BVA"),
            ("Boundary", "BVA"), ("EP", "EP"), ("Basis", "White-box path/branch"),
            ("Branch", "White-box path/branch"), ("Condition", "White-box path/branch"),
            ("Data-flow", "White-box data-flow"), ("API", "API"), ("Security", "Security (STRIDE)"),
            ("UI automation", "Selenium UI"), ("GUI", "GUI checklist"), ("Configuration", "Configuration"),
            ("Accessibility", "WCAG review"), ("Compatibility", "Compatibility"), ("Performance", "Load/stress")]


def tech_family(t):
    return next(name for key, name in FAMILIES if t.startswith(key))


def compress_ids(ids):
    """TC-BB-001, TC-BB-002, TC-BB-003 -> TC-BB-001-003."""
    out, run = [], []

    def flush():
        if not run:
            return
        out.append(run[0] if len(run) == 1 else f"{run[0]}-{run[-1].split('-')[-1]}")

    for i in ids:
        pre, num = i.rsplit("-", 1)
        if run and run[-1].rsplit("-", 1)[0] == pre and int(run[-1].rsplit("-", 1)[1]) + 1 == int(num):
            run.append(i)
        else:
            flush()
            run = [i]
    flush()
    return ", ".join(out)


# --------------------------------------------------------------------------- markdown outputs
def md_table(headers, rows):
    esc = lambda v: str(v).replace("|", "\\|").replace("\n", " ")  # noqa: E731
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)] +
                     ["| " + " | ".join(esc(v) for v in r) + " |" for r in rows]) + "\n"


def write(path, text):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as fh:
        fh.write(text)


def markdown(cases, rtm_rows):
    write("07_Test_Management/RTM.md",
          "# Requirements Traceability Matrix\n\nGenerated from `tools/test_catalogue.py`. Uses the RTM "
          "template from the Group Project 2 brief. Every requirement has at least one executed test.\n\n"
          + md_table(["Requirement/Feature", "Test Scenario", "Test Case ID(s)", "Test Type/Technique",
                      "Result", "Defect ID"], rtm_rows))
    parts = ["# Defect Reports (all confirmed defects)\n\nDefect Report Template from the brief. Lifecycle used: "
             "New -> Confirmed (reproduced by a second member). As an independent QA team we do not fix code, "
             "so Retest/Closed happen after the developers fix a defect (run `pytest -m regression`).\n"]
    sev = Counter(d["Severity"] for d in T.DEFECTS)
    parts.append(md_table(["Severity", "Count"], [[k, sev[k]] for k in ("Critical", "Major", "Moderate", "Minor")]))
    for d in T.DEFECTS:
        parts.append(f"\n## {d['Defect ID']}: {d['Title']}\n\n" +
                     md_table(["Field", "Value"], [[k, v] for k, v in d.items() if k not in ("Defect ID", "Title")]))
    write("07_Test_Management/Defect_Reports.md", "".join(parts))

    reg = [c for c in cases if c["Regression"] == "Yes"]
    write("06_Automation_Regression/Regression_Suite.md",
          "# Focused Regression Suite\n\nRun: `pytest -m regression` (add `and not ui` without a browser).\n\n"
          "Selection rules: high-risk areas, frequently used features, critical business rules and **every "
          "failed boundary**. Failing tests are known defects; after a fix they act as confirmation tests, "
          "and the passing ones check that the fix broke nothing.\n\n"
          f"Size: {len(reg)} tests - {sum(c['Status'] == 'Pass' for c in reg)} pass, "
          f"{sum(c['Status'] == 'Fail' for c in reg)} fail.\n\n" +
          md_table(["Test", "Feature", "Objective", "Status", "Defect"],
                   [[c["Test Case ID"], c["Feature/Requirement"], c["Objective"], c["Status"], c["Defect ID"]]
                    for c in reg]))

    at = [c for c in cases if c["Test Case ID"].startswith("AT-")]
    write("06_Automation_Regression/Manual_to_Automated_Traceability.md",
          "# Manual-to-Automated Traceability\n\nUI scripts (Selenium, Page Object Model) mapped to the manual "
          "cases they automate. The 137 non-UI automated tests keep the SAME IDs as their manual design "
          "(e.g. `test_tc_bb_010` automates TC-BB-010), so they are traced one-to-one.\n\n" +
          md_table(["Script", "What it automates", "Manual test(s)", "Requirement", "Result", "Defect"],
                   [[c["Test Case ID"], c["Objective"], T.AT_MAP[c["Test Case ID"]], c["Feature/Requirement"],
                     c["Status"], c["Defect ID"]] for c in at]) +
          "\n## Automated vs manual by phase\n\n" +
          md_table(["Phase", "Automated", "Manual", "Script / location"],
                   [[v[0], sum(c["Phase"] == v[0] and c["Automated"] == "Yes" for c in cases),
                     sum(c["Phase"] == v[0] and c["Automated"] == "No" for c in cases), v[1]]
                    for v in T.PHASES.values()]))

    # metrics summary
    st = Counter(c["Status"] for c in cases)
    ex = st["Pass"] + st["Fail"] + st["Blocked"]
    auto = sum(c["Automated"] == "Yes" for c in cases)
    rows = []
    for k, (ph, _) in T.PHASES.items():
        pc = [c for c in cases if c["Phase"] == ph]
        s = Counter(c["Status"] for c in pc)
        e = s["Pass"] + s["Fail"] + s["Blocked"]
        rows.append([ph, len(pc), e, s["Pass"], s["Fail"], s["Not Run"], f"{100 * s['Pass'] / e:.1f}%"])
    rows.append(["**Total**", len(cases), ex, st["Pass"], st["Fail"], st["Not Run"], f"{100 * st['Pass'] / ex:.1f}%"])
    sev = Counter(d["Severity"] for d in T.DEFECTS)
    area = Counter(d["Area"] for d in T.DEFECTS)
    write("08_Final_QA_Report/Metrics.md",
          "# Test and Defect Metrics\n\nGenerated by `tools/build_documents.py` (live formulas are in "
          "`07_Test_Management/PyTodo_Test_Management.xlsx`, sheets *Execution Status* and *Metrics*).\n\n" +
          md_table(["Phase", "Planned", "Executed", "Passed", "Failed", "Not Run", "Pass rate"], rows) +
          "\n" + md_table(["Metric", "Value"], [
              ["Execution rate", f"{ex}/{len(cases)} = {100 * ex / len(cases):.1f}%"],
              ["Pass rate", f"{st['Pass']}/{ex} = {100 * st['Pass'] / ex:.1f}%"],
              ["Automation rate", f"{auto}/{len(cases)} = {100 * auto / len(cases):.1f}%"],
              ["Confirmed defects (Critical + Major)", f"{len(T.DEFECTS)} ({sev['Critical'] + sev['Major']})"],
              ["Defect density", f"{len(T.DEFECTS)} / 0.557 KLOC = {len(T.DEFECTS) / 0.557:.1f} per KLOC"],
              ["Coverage helpers.py (stmt / branch)", "100% / 100%"],
              ["Coverage app.py (stmt / branch)", "98.3% / 89.1%"]]) +
          "\n" + md_table(["Severity", "Count"], [[k, sev[k]] for k in ("Critical", "Major", "Moderate", "Minor")]) +
          "\n" + md_table(["Area", "Count"], area.most_common()) +
          "\nCharts: `charts/results_by_phase.png`, `charts/defects_by_severity.png`, "
          "`charts/defects_by_area.png`, `charts/p95_by_users.png`.\n")

    api = [c for c in cases if c["Test Case ID"].startswith("TC-API")]
    json.dump([{"id": c["Test Case ID"], "objective": c["Objective"], "request": c["Test Data"],
                "expected": c["Expected Result"]} for c in api],
              open(os.path.join(ROOT, "04_Web_API", "api_request_data.json"), "w"), indent=2)


def simple_sheet(wb, name, headers, rows, widths=None, status_col=None):
    ws = wb.create_sheet(name[:31])
    write_table(ws, headers, [list(r) for r in rows], widths=widths, status_col=status_col)
    return ws


def summary_sheet(wb, case_sheet_name, n):
    ws = wb.create_sheet("Execution Summary")
    write_table(ws, ["Measure", "Value"], [], widths={"Measure": 30, "Value": 14})
    ref = f"'{case_sheet_name}'!$J$2:$J${n + 1}"
    rows = [("Planned", f"=COUNTA({ref})", "0"), ("Passed", f'=COUNTIF({ref},"Pass")', "0"),
            ("Failed", f'=COUNTIF({ref},"Fail")', "0"), ("Blocked", f'=COUNTIF({ref},"Blocked")', "0"),
            ("Not Run", f'=COUNTIF({ref},"Not Run")', "0"), ("Executed", "=B3+B4+B5", "0"),
            ("Execution rate", "=IF(B2=0,0,B7/B2)", "0.0%"), ("Pass rate", "=IF(B7=0,0,B3/B7)", "0.0%")]
    for i, (k, f, fmt) in enumerate(rows, start=2):
        ws.cell(row=i, column=1, value=k).font = Font(name=FONT, size=10)
        c = ws.cell(row=i, column=2, value=f)
        c.number_format = fmt
        c.font = Font(name=FONT, size=10)
        for col in (1, 2):
            ws.cell(row=i, column=col).border = BORDER
    ws.cell(row=11, column=1, value=f"Formulas count the Status column of '{case_sheet_name}'.").font = Font(
        name=FONT, italic=True, size=9)


def defect_sheet(wb, defect_ids):
    dh = list(T.DEFECTS[0].keys())
    rows = [[d[h] for h in dh] for d in T.DEFECTS if d["Defect ID"] in defect_ids]
    simple_sheet(wb, "Defect Log", dh, rows,
                 widths={"Defect ID": 10, "Title": 40, "Steps to Reproduce": 40, "Expected Result": 30,
                         "Actual Result": 36, "Environment": 26, "Evidence": 30, "Preconditions": 22})


def weekly_workbooks(cases):
    import weekly_data as W
    by = lambda p: [c for c in cases if c["Test Case ID"].startswith(p)]  # noqa: E731
    defects_of = lambda cs: sorted({c["Defect ID"] for c in cs if c["Defect ID"]})  # noqa: E731
    cols = TEMPLATE + ["Priority"]

    def cases_sheet(wb, name, cs):
        ws = wb.create_sheet(name)
        write_table(ws, cols, [[c[h] for h in cols] for c in cs], status_col="Status")

    def save(wb, folder, week):
        wb.save(os.path.join(ROOT, folder, f"PyTodo QA Data Collection (Week {week}).xlsx"))

    # Week 1
    wb = Workbook(); wb.remove(wb.active)
    simple_sheet(wb, "Feature Scope Matrix", ["ID", "Feature", "Business rule", "Entry point", "Likelihood (1-3)",
                                              "Impact (1-3)", "Risk score", "Priority", "Techniques", "In scope"],
                 [[r[0], r[1], r[2], r[3], r[4], r[5], None, None, r[6], r[7]] for r in W.SCOPE],
                 widths={"Business rule": 46, "Techniques": 30, "Entry point": 20})
    ws = wb["Feature Scope Matrix"]
    for i in range(2, len(W.SCOPE) + 2):
        ws[f"G{i}"] = f"=E{i}*F{i}"
        ws[f"H{i}"] = f'=IF(G{i}>=6,"High",IF(G{i}>=4,"Medium","Low"))'
    bb = by("TC-BB")
    cases_sheet(wb, "Test Cases", bb)
    summary_sheet(wb, "Test Cases", len(bb))
    defect_sheet(wb, defects_of(bb))
    save(wb, "01_Black_Box", 1)
    # Week 2
    wb = Workbook(); wb.remove(wb.active)
    wbc = by("TC-WB")
    simple_sheet(wb, "Unit Selection & V(G)", ["Unit", "Why selected", "V(G)", "Tests"], W.UNITS,
                 widths={"Unit": 34, "Why selected": 60, "Tests": 18})
    cases_sheet(wb, "Test Cases", wbc)
    simple_sheet(wb, "Coverage", ["Scope", "Measured on real app", "Not executed", "How to reproduce"], [
        ("helpers.py", "100% of executable lines", "none", "python tools/statement_coverage.py"),
        ("app.py", "all but 5 lines", "242, 266 (GET forms – Selenium only), 375 (API status=open – gap), 481–482 (start-up)",
         "python tools/statement_coverage.py"),
        ("Branch coverage", "helpers.py 18/18; app.py 57/64 (team pytest-cov run)", "–",
         "pytest -m \"not ui\" --cov=app --cov=helpers --cov-branch")],
        widths={"Scope": 16, "Measured on real app": 40, "Not executed": 60, "How to reproduce": 50})
    summary_sheet(wb, "Test Cases", len(wbc))
    defect_sheet(wb, defects_of(wbc))
    save(wb, "02_White_Box_Coverage", 2)
    # Week 3
    wb = Workbook(); wb.remove(wb.active)
    gui, acc, comp = by("TC-GUI"), by("TC-ACC"), by("TC-COMP")
    cases_sheet(wb, "GUI Checklist", gui)
    simple_sheet(wb, "Compatibility Matrix", ["Browser / OS", "Desktop 1366x768", "Tablet 768x1024",
                                              "Phone 375x812", "Test case", "Status"], W.COMPAT,
                 widths={"Browser / OS": 22, "Test case": 26, "Status": 36})
    cases_sheet(wb, "Compatibility Cases", comp)
    simple_sheet(wb, "Usability Observations", ["LEMES dimension", "Positive", "Issue", "Defect"], W.USABILITY,
                 widths={"Positive": 40, "Issue": 55})
    cases_sheet(wb, "Accessibility Review", acc)
    all3 = gui + acc + comp
    ws = wb.create_sheet("All Week 3 Cases")
    write_table(ws, cols, [[c[h] for h in cols] for c in all3], status_col="Status")
    summary_sheet(wb, "All Week 3 Cases", len(all3))
    defect_sheet(wb, defects_of(all3))
    save(wb, "03_Special_Testing", 3)
    # Week 4
    wb = Workbook(); wb.remove(wb.active)
    api = by("TC-API")
    simple_sheet(wb, "Web Test Scenarios", ["ID", "Scenario", "Steps", "Covered by", "Result"], W.WEB_SCENARIOS,
                 widths={"Scenario": 28, "Steps": 50, "Covered by": 36})
    cases_sheet(wb, "API Test Suite", api)
    simple_sheet(wb, "Request Test Data", ["Test Case ID", "Request", "Expected status / body"],
                 [(c["Test Case ID"], c["Test Data"], c["Expected Result"]) for c in api],
                 widths={"Request": 60, "Expected status / body": 50})
    simple_sheet(wb, "UI vs API Comparison", ["Input", "Browser (UI)", "Server / API", "Defect"], W.UI_VS_API,
                 widths={"Input": 28, "Browser (UI)": 36, "Server / API": 44})
    summary_sheet(wb, "API Test Suite", len(api))
    defect_sheet(wb, defects_of(api))
    save(wb, "04_Web_API", 4)
    # Week 5
    wb = Workbook(); wb.remove(wb.active)
    sec, perf = by("TC-SEC"), by("TC-PERF")
    simple_sheet(wb, "STRIDE Threats", ["Asset / function", "STRIDE", "Threat", "Property", "Test(s)", "Result"],
                 W.STRIDE, widths={"Asset / function": 24, "Threat": 50, "Result": 34})
    cases_sheet(wb, "Security Test Cases", sec)
    simple_sheet(wb, "Performance Plan", ["Item", "Value"], W.PERF_PLAN, widths={"Item": 16, "Value": 100})
    simple_sheet(wb, "Performance Results", ["Users", "Task list avg / p95 (ms)", "Dashboard avg / p95 (ms)",
                                             "Login avg / p95 (ms)", "Req/s", "Errors", "Result"], W.PERF_RESULTS)
    cases_sheet(wb, "Performance Cases", perf)
    simple_sheet(wb, "Limits & Recommendations", ["Area", "Limitation", "Recommendation"], W.LIMITS,
                 widths={"Limitation": 60, "Recommendation": 60})
    summary_sheet(wb, "Security Test Cases", len(sec))
    defect_sheet(wb, defects_of(sec + perf))
    save(wb, "05_Security_Performance", 5)
    # Week 6
    wb = Workbook(); wb.remove(wb.active)
    simple_sheet(wb, "Automation Candidates", ["Candidate group", "Repetition", "Stable", "Critical",
                                               "Regression value", "Decision"], W.CANDIDATES,
                 widths={"Candidate group": 40, "Decision": 30})
    at = by("AT-")
    simple_sheet(wb, "Test Traceability", ["Automated test", "What it automates", "Manual test(s)", "Requirement",
                                           "Script", "Status", "Defect"],
                 [(c["Test Case ID"], c["Objective"], T.AT_MAP[c["Test Case ID"]], c["Feature/Requirement"],
                   "06_Automation_Regression/test_ui_selenium.py", c["Status"], c["Defect ID"]) for c in at],
                 widths={"What it automates": 34, "Manual test(s)": 26, "Script": 40}, status_col="Status")
    auto = [c for c in cases if c["Automated"] == "Yes"]
    simple_sheet(wb, "Automated Test Results", ["Automated test", "Script / function", "Expected", "Actual",
                                                "Status", "Evidence"],
                 [(c["Test Case ID"], f"test_{c['Test Case ID'].lower().replace('-', '_')}", c["Expected Result"],
                   c["Actual Result"], c["Status"], c["Evidence"]) for c in auto],
                 widths={"Script / function": 20, "Expected": 40, "Actual": 44, "Evidence": 60}, status_col="Status")
    reg = [c for c in cases if c["Regression"] == "Yes"]
    simple_sheet(wb, "Regression Suite", ["Order", "Test", "Feature", "Objective", "Expected", "Latest status",
                                          "Defect"],
                 [(i, c["Test Case ID"], c["Feature/Requirement"], c["Objective"], c["Expected Result"], c["Status"],
                   c["Defect ID"]) for i, c in enumerate(reg, 1)],
                 widths={"Objective": 40, "Expected": 40}, status_col="Latest status")
    simple_sheet(wb, "Automation Reflection", ["Area", "Observation", "Evidence", "Recommendation"], W.REFLECTION,
                 widths={"Observation": 60, "Evidence": 40, "Recommendation": 40})
    save(wb, "06_Automation_Regression", 6)


def main():
    cases, changed = merged_cases()
    by = lambda p: [c for c in cases if c["Test Case ID"].startswith(p)]  # noqa: E731
    weekly_workbooks(cases)
    rtm_rows = master_workbook(cases)
    markdown(cases, rtm_rows)
    st = Counter(c["Status"] for c in cases)
    print(f"{len(cases)} test cases: {dict(st)}; {len(T.DEFECTS)} defects")
    if changed:
        print("Status changed by latest PyTest run (update the report!):")
        for c in changed:
            print("  ", *c)


if __name__ == "__main__":
    main()
