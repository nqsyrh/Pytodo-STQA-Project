# Live Demonstration Script

**Target time:** 4–5 minutes. Follow the lecturer's time allocation if it is different.
**Presenter:** [Automation coordinator name]. Speakers must be assigned and the demo rehearsed on the presentation laptop. This file does not claim that a rehearsal has taken place.

## 1. Preparation (the day before)

The app in `app/` is the supplied copy and has not been modified. Every test creates its own temporary SQLite database and disposable accounts (`qa_user1`, `qa_user2`), so the demo never touches real data.

Run these in **PowerShell** from the repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-test.txt
python -m pytest test_setup_check.py -v        # must be all green before the demo
```

Then do one full rehearsal of section 3 and **screen-record it** as `demo_backup.mp4`. The video is your fallback.

Checklist for presentation day: laptop charged · virtual environment activated · Chrome installed · terminal font enlarged · `PyTodo_Test_Management.xlsx` already open · `demo_backup.mp4` on the desktop.

## 2. The core demo: one requirement, three tests (about 2 minutes)

**Requirement:** a user may see and delete only their own tasks.

```powershell
python -m pytest -k "tc_api_043 or tc_api_024 or tc_api_042" -v --tb=short
```

**Expected result on the supplied app: 2 passed, 1 failed.** The exit code is 1 because the ownership test fails. That failure is the product defect, so do not change the expected result to make it pass.

| Test | What it checks | Expected | Say |
|---|---|---|---|
| TC-API-043 | DELETE without logging in | **PASS**: HTTP 401 | "Logged-out users are blocked." |
| TC-API-024 | qa_user1 GETs qa_user2's task | **PASS**: HTTP 404 | "Reading someone else's task is blocked." |
| TC-API-042 | qa_user1 DELETEs qa_user2's task | **FAIL**: `assert (200 in (403, 404))` | "But deleting it is allowed: the server answers 200 and the task is gone." |

Then open **DEF-005** in `07_Test_Management/Defect_Reports.md` and explain:
- steps, expected result versus actual result, and the classification **Critical**
- source review: `DELETE /api/tasks/<id>` deletes by ID without checking `user_id`, while the GET route does check it
- the message: "Each endpoint must check ownership on its own. Passing a GET test proves nothing about DELETE. After a fix, this test becomes the regression check."

Verified in this package: `evidence/demo_check_log.txt` and `evidence/demo_check_results.xml` (2 pass, 1 fail).

## 3. Optional extras, if time allows (about 2–3 minutes)

| Step | Command / action | Expected | Say |
|---|---|---|---|
| Unit tests | `python -m pytest -m unit -q` | 26 passed, 3 failed | "Every statement and branch of helpers.py runs, yet 3 tests fail: coverage is not correctness." (DEF-001, 002, 003) |
| API + security suite | `python -m pytest 04_Web_API 05_Security_Performance -q` | 34 passed, 25 failed | "Each failure message names its DEF id." |
| UI defect in the browser | `$env:HEADLESS="0"; python -m pytest -m ui -k "at_004" -v` (needs the app running in a second window: `cd app; python app.py`) | Chrome drives itself; AT-004 fails | "A task due today shows Overdue: DEF-001, found by boundary value analysis, seen end-to-end with the Page Object Model." |
| Traceability | Show the *RTM* and *Metrics* sheets in `07_Test_Management/PyTodo_Test_Management.xlsx` | Live formulas | "One test catalogue feeds every artefact." |
| CI | Show `.github/workflows/qa.yml` (and the Actions tab, if it has run on GitHub) | Pipeline stages | "Bandit would flag the hard-coded secret and the f-string SQL. Known failures keep the gate red until they are fixed." |

The figures above come from the run recorded in `07_Test_Management/Execution_Evidence/` (Python 3.13, Flask 3.1.3, pytest 9.1.1). A new run on a different setup may differ slightly. If it does, say so and save the new output. Never present an old result as a new live run.

## 4. Fallback

If the environment fails, **do not debug on stage.** Instead:
1. Play `demo_backup.mp4` from the same step.
2. Or show the saved logs: `09_Presentation/evidence/demo_check_log.txt`, then `07_Test_Management/Execution_Evidence/pytest_all.log` and `run_full_suite_summary.png`.

Introduce them as "our saved run from 27 November 2026", not as a live result.

## 5. Questions to rehearse

- **Why does 100% helper coverage still have failures?** Coverage shows which code ran. Assertions check whether the result was right. The boundary rules themselves are wrong.
- **Why does GET pass while DELETE fails?** The GET route and the web delete form check `user_id`, but the API DELETE route (app.py line 459) does not. Each endpoint must enforce it independently.
- **Why not release with a 71.6% pass rate?** One reproduced vulnerability that deletes other users' data outweighs any pass percentage.
- **Why 183 test cases but only 137 tests in the verified pytest run?** 183 = 137 pytest tests + 10 Selenium tests (run separately in Chrome, Edge and Firefox) + 36 manual checks (GUI, usability, accessibility, compatibility). Each group's evidence is in its week folder, and none is counted twice.
- **Do you claim ISO compliance or a CMMI level?** No. We used the standards as frameworks. No certification or appraisal took place.
- **Did you fix the app?** No. The assignment evaluates the supplied source, so it is unmodified. We recommend fixes only.
