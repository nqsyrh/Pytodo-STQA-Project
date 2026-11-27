# 06 – Test Automation and Regression (Project Week 6)

| Brief deliverable | File |
|---|---|
| **Screenshot evidence** | `week 6 evidence/run_regression_suite.png` – regression run on the real app; Selenium screenshots go to `week 6 evidence/selenium_screenshots/` |
| Automation candidate justification | `Automation_Candidates_and_Reflection.md` §1 |
| Automated scripts | `test_ui_selenium.py`, `pages/` (Page Object Model), plus suites in 01, 02, 04, 05 |
| Manual-to-automated traceability | `Manual_to_Automated_Traceability.md` (generated) |
| Execution report / logs | `reports/junit_*.xml`, `week 6 evidence/` |
| Regression suite and automation reflection | `Regression_Suite.md` (52 tests) · `Automation_Candidates_and_Reflection.md` §3 |

**Results:** Selenium 7/10 pass (AT-002, 004 and 008 fail on DEF-002, 001 and 007). Regression suite: 52 tests, 28 pass and 24 fail (known defects).

```bash
cd app && python app.py                 # terminal 1
pytest -m ui                            # AT-001..010, headless Chrome
HEADLESS=0 BROWSER=firefox pytest -m ui # watch it in Firefox
pytest -m regression                    # 52-test regression suite
```
