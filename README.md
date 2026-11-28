# PyTodo Pro – Software Testing and Quality Assurance Project

**Course:** TFB3433 Software Testing and Quality Assurance

**Semester:** September 2026

**Lecturer:** Dr. Abdullateef Oluwagbemiga Balogun

**Application under test:** PyTodo Pro

## Team details

This project was completed by the following group members (Information Technology):

| Name | Student ID | 
|---|---|
| Nureen Nellysha Binti Norazizi | 22006973 | 
| Nurul Afiqah Insyirah Binti Abu | 22002020 |

## Project overview

This repository contains a progressive, independent quality evaluation of PyTodo Pro, a Flask and SQLite task-management web application. We evaluated the supplied application rather than developing or repairing it. The code in `app/` is the lecturer's copy, and its SHA-256 hashes are recorded.

Testing covers:
- black-box test design (EP, BVA, decision tables, state transitions)
- selected white-box paths and code coverage
- GUI, usability, accessibility and compatibility checks
- REST API behaviour
- STRIDE-based security tests on a local copy only
- controlled performance experiments
- automated regression with PyTest and Selenium
- traceability, defect management and the final quality evaluation

**Verdict: PyTodo Pro is not ready for release.** Five Critical defects are open:
- cross-user task deletion
- SQL injection in search
- stored XSS
- an invalid due date that crashes the task list
- a hard-coded secret key with debug mode on

Testing shows that defects are present. It cannot prove the application is defect-free.

## Repository structure

| Folder | Contents |
|---|---|
| `01_Black_Box` | Week 1 application analysis, feature/risk matrix, black-box test design, Week 1 Data Collection workbook, `test_black_box.py`, **week 1 evidence** (49 screenshots) |
| `02_White_Box_Coverage` | Week 2 unit selection, control-flow graph and V(G), unit tests, coverage results, **week 2 evidence** (31 screenshots) |
| `03_Special_Testing` | Week 3 GUI checklist, compatibility matrix, usability (LEMES) and WCAG 2.1 review, **week 3 evidence** (17 page screenshots) |
| `04_Web_API` | Week 4 web scenarios, 46 API tests, request data, UI vs API comparison, **week 4 evidence** (46 screenshots) |
| `05_Security_Performance` | Week 5 STRIDE table, 14 security tests, Locust performance plan and results, **week 5 evidence** (14 screenshots) |
| `06_Automation_Regression` | Week 6 automation candidates, Selenium Page Object Model, manual-to-automated traceability, 52-test regression suite, reflection, **week 6 evidence** |
| `07_Test_Management` | Formal test plan and strategy (IEEE 829), master test repository, RTM, defect log, risk register, execution status, **Execution_Evidence** (verified run logs and hashes) |
| `08_Final_QA_Report` | Final integrated QA report (Word and PDF), metrics and charts, residual risk assessment |
| `09_Presentation` | Presentation outline, live-demo script, standards integration (ISO/IEC 25010, ISO 9001, CMMI, CI/CD, Agile/DevOps) |
| `app` | The unmodified PyTodo Pro application under test |
| `tools` | Test catalogue (single source of truth) and the scripts that rebuild every document and capture evidence |
| `.github/workflows` | CI/CD pipeline with quality gates (static analysis → unit → API regression → UI smoke → nightly) |

Each week folder has its own README, which maps the brief's deliverables to files, and a **`PyTodo QA Data Collection (Week N).xlsx`** workbook.

## Tools and environment

- Python 3.13.18 for the verified run on 27 November 2026 (the app itself requires Flask 3.0.3; the run used Flask 3.1.3 and Werkzeug 3.1.9)
- pytest 9.1.1, pytest-cov / coverage.py, Flask test client
- Selenium 4 with the Page Object Model for UI automation
- axe-core for the accessibility scan
- Locust for performance experiments
- Google Chrome for GUI checks and screenshot evidence (desktop 1366×768, tablet 768×1024, phone 375×812)
- openpyxl for the workbooks, GitHub Actions for CI

Full environment details and file hashes: `07_Test_Management/Execution_Evidence/environment.txt`.

## Setup

From the repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1                 # macOS/Linux: source .venv/bin/activate
python -m pip install -r app/requirements.txt -r requirements-test.txt
python -m pytest test_setup_check.py -v    # checks the tests match the app
```

Run the application:

```powershell
cd app
python app.py
```

Open http://127.0.0.1:5000/ and register a disposable local account.

## Automated tests

Run all non-UI suites (black-box, white-box, API, security):

```powershell
python -m pytest -m "not ui" -v
```

Other commands:

| Command | What runs |
|---|---|
| `python -m pytest -m unit` | White-box unit tests (29) |
| `python -m pytest -m regression` | Focused regression suite (52) |
| `python -m pytest -m ui` | Selenium AT-001..010 (start the app first) |
| `python -m pytest -m "not ui" --cov=app --cov=helpers --cov-branch --cov-report=term-missing` | Statement and branch coverage |
| `bash 05_Security_Performance/performance/run_performance.sh` | Locust load levels 1/10/25/50 and stress 100 |
| `QA_EVIDENCE=1 python -m pytest -m "not ui"` then `python tools/capture_week_evidence.py` | Regenerate the screenshot card for every test |
| `python tools/build_documents.py` | Rebuild all workbooks, RTM and metrics from the results |

Known failures must stay visible until the developers fix the defects. Each failing test asserts the correct behaviour from the requirements and is tagged with its defect ID (`@pytest.mark.defect("DEF-xxx")`). Do not change expected results just to make the suite pass.

## Current evidence summary

- **Test cases:** 183 planned, **183 executed (100%)**, 131 passed, 52 failed (pass rate 71.6%).
- **Verified automated run on the real app (27 Nov 2026):** 137 tests, 100 passed and 37 failed. The 37 failures are exactly the defects in the report.
- **Regression suite:** 52 tests, 28 passed and 24 failed (known defects).
- **Defects:** 26 confirmed: 5 Critical, 5 Major, 7 Moderate and 9 Minor. Every failed test is linked to a defect ID.
- **Coverage:** helpers.py 100% statement and branch coverage, while three assertions still fail. app.py misses only lines 242, 266, 375, 481 and 482.
- **Performance:** task list and dashboard p95 stayed ≤ 12 ms at 50 users. Login is the bottleneck in bursts (p95 1,200 ms at 25 users). These are local trends, not production capacity.
- **Accessibility:** a basic WCAG 2.1 review. The app does not reach Level AA (unlabelled fields, contrast, reflow).
- **Compatibility:** Chrome 158, Edge 158 and Firefox 161 on Windows 11 (member laptops) and Chrome 153 on Linux all pass the smoke set on desktop and tablet; the 10 Selenium tests give 7 pass / 3 fail in every browser (the same three defects). The phone layout fails everywhere (DEF-023). Safari is out of scope (no Mac).
- **Screenshot evidence:** 159 images across the `week N evidence` folders. Each automated test card shows the real request and response, the page the app rendered, PASS/FAIL, and the test code.

## Final submission

- Final report: `08_Final_QA_Report/PyTodo_Pro_QA_Report.pdf` (Word: `PyTodo_Pro_QA_Report.docx`)
- Live demonstration script: `09_Presentation/Live_Demo_Script.md`
