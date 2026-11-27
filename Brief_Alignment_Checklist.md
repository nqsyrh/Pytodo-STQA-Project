# Brief Alignment Checklist (Group Project 2 → this repository)

Status key: ✅ done · ⚠ team action needed before submission

## Weekly deliverables

| Brief week | Required deliverable | Where | Status |
|---|---|---|---|
| 1 | Application overview, feature inventory | `01_Black_Box/Feature_Inventory_and_Risk_Matrix.md` | ✅ |
| 1 | Initial test scope / risk matrix | same, §3 | ✅ |
| 1 | EP, BVA, decision-table, state-transition cases | `01_Black_Box/Black_Box_Test_Design.md`, `PyTodo QA Data Collection (Week 1).xlsx` | ✅ |
| 1 | Tests executed; expected and actual recorded | Expected/actual in workbook; scripted execution justified in report §2.0; screenshots from the real app | ✅ |
| 1 | Initial defect records | `07_Test_Management/Defect_Reports.md` | ✅ |
| 2 | Unit selection and justification, control flow, V(G) | `02_White_Box_Coverage/White_Box_Analysis.md` | ✅ |
| 2 | Statement/branch tests, path/data-flow discussion | same + `test_helpers_unit.py` | ✅ |
| 2 | Coverage report and interpretation | §4 + `07_Test_Management/Execution_Evidence/statement_coverage.txt` (measured on the real app) | ✅ (branch %: run `tools/run_all.sh` with pytest-cov to regenerate `coverage_html/`) |
| 3 | GUI checklist, usability, WCAG, screenshots | `03_Special_Testing/` with 17 screenshots from the real app | ✅ (optional: axe JSON via `scripts/axe_scan.py`) |
| 3 | Compatibility matrix | `03_Special_Testing/Compatibility_Matrix.md` | ✅ Chrome, Edge and Firefox on Windows 11 + Chrome on Linux executed (4/4 pass); Safari out of scope |
| 4 | Web scenarios, API suite, request data, expected vs actual, UI vs API | `04_Web_API/` | ✅ |
| 5 | STRIDE table, safe security tests | `05_Security_Performance/STRIDE_Threat_Model.md`, `test_security.py` | ✅ |
| 5 | Performance objective, workload, environment, results, limitations | `Performance_Test_Report.md`, `performance/` | ✅ (raw Locust CSVs: re-run `run_performance.sh`) |
| 5 | TC-SEC-013 screenshot | `05_Security_Performance/week 5 evidence/werkzeug_debugger_TC-SEC-013.png` | ✅ |
| 6 | Automation candidates, scripts, manual-to-auto map, logs, regression suite, reflection | `06_Automation_Regression/` | ✅ |
| 7 | Test plan, strategy, RTM, master repository, defect log, execution status | `07_Test_Management/` | ✅ |
| 8 | Final report, metrics, residual risk, limitations, recommendations | `08_Final_QA_Report/` | ✅ |
| 9 | ISO/IEC 25010, CI/CD, Agile/DevOps, presentation, live demo | `09_Presentation/`, `.github/workflows/qa.yml` | ⚠ build the slides from `Presentation_Outline.md`; record a backup demo |

## Templates

| Template | Required fields present? | Where |
|---|---|---|
| Test Case Template (12 fields) | ✅ all 12 + priority, automation, regression | every `*_Test_Cases.xlsx`, Master Test Repository |
| Defect Report Template (13 fields) | ✅ all 26 defects in full (the report shows one full example) | `Defect_Reports.md`, sheet *Defect Log* |
| RTM Template (6 columns) | ✅ incl. Test Scenario and Technique | `RTM.md`, sheet *RTM* (the report's §9 table is a 4-column summary) |

## Final Submission Checklist (brief p. 6–7)

| Item | Status |
|---|---|
| All deliverables in the shared repository | ✅ (see ⚠ above for evidence files) |
| README explains setup and automated-test execution | ✅ `README.md` |
| Unique test case IDs with expected and actual results | ✅ 183 IDs |
| RTM current and consistent with the test repository | ✅ generated from the same catalogue |
| Defect IDs and statuses consistent across artefacts | ✅ checked by script: every failed case → one defect, every defect → its tests |
| Automated scripts execute in the documented environment | ✅ verified on the real app: 100 pass / 37 fail, logs in `07_Test_Management/Execution_Evidence/` |
| Performance results state workload and environment | ✅ |
| Metrics calculated correctly and interpreted | ✅ live formulas in workbook; interpretation in report §11 |
| Final report states limitations and residual risks | ✅ |
| Presentation includes a prepared live demonstration | ✅ script ready; ⚠ rehearse and record the backup |

## Corrections made to the report (copy in `08_Final_QA_Report/`)

- §9 RTM, row F03: `TC-SEC-002–003` was listed twice, which inflated the result to "9/13 passed". Corrected to **8/11 passed**.
- Cover page and §1.3: team names and student IDs filled in.
- Table of contents, list of tables and list of figures populated; the "right-click to update" note removed.
