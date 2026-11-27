# Software Test Plan and Test Strategy – PYTODO-STP v2.0

| Item | Value |
|---|---|
| Identifier | PYTODO-STP v2.0 (v1.0 Week 1 draft; v2.0 Week 7, updated with evidence from Weeks 1–6) |
| Standard | Structure follows IEEE 829-2008 |
| Owner | QA / Test Lead (Nureen Nellysha Binti Norazizi); reviewed by all members |

## 1. Introduction and objectives
Verify features F01–F12 against the README and `helpers.py`. Find reproducible defects. Measure coverage of the selected units. Evaluate security, performance, usability, accessibility and compatibility. Build a regression suite. Give an evidence-based quality judgement, without claiming the software is defect-free.

## 2. Test items and scope
**In scope:** PyTodo Pro as issued (`app.py`, `helpers.py`, templates, SQLite DB); F01–F12 through the UI and the API; NF2 performance, NF3 GUI/usability, NF4 accessibility and NF5 compatibility; security through STRIDE.
**Out of scope:** changing the code, production hosting, load beyond one machine, uncontrolled penetration testing, testing with real users who have disabilities, Safari / macOS (no member has a Mac; the group tests Chrome, Edge and Firefox).

## 3. Approach (summary – details in §9 Strategy)
Risk-based. Black-box (EP, BVA, decision table, state transition) → white-box (basis path, branch, data-flow) → special testing (GUI, WCAG, compatibility) → API → STRIDE security and Locust performance → automation and regression.

## 4. Environment, tools and test data
| Item | Value |
|---|---|
| OS / runtime | Linux; Python 3.13; Flask 3.0.3; SQLite |
| Browsers | Chrome 153 (Linux); Chrome 158, Edge 158 and Firefox 161 on Windows 11 (member laptops); headless Chrome 153 on Linux (verification run) |
| Tools | PyTest, pytest-cov, Flask test client, Selenium 4 (POM), axe-core, Locust, openpyxl, GitHub + Actions |
| Test data | users `qa_user1`, `qa_user2`; boundary usernames (2, 3, 4, 19, 20, 21 chars) and passwords (7, 8, 9 chars); dates today −1 … +3; titles that are empty, spaces only, HTML, or 5,000 characters; apostrophes; impossible dates; `perf_user` with 100 tasks |
| Isolation | fresh temporary database per test; app code never modified |

## 5. Pass / fail, suspension and resumption criteria
- **Pass:** actual result matches the expected result written before execution. **Fail:** it differs (the case is linked to a defect). **Blocked:** a precondition cannot be met. **Not Run:** planned but not executed (reason recorded).
- **Suspend** if the app cannot start, the database is corrupted (DEF-008), or more than 30% of a suite is blocked. **Resume** after resetting the database.

## 6. Entry and exit criteria
| Criterion | Type | Target | Actual | Met? |
|---|---|---|---|---|
| App runs; cases have IDs, data and expected results; fresh DB per run | Entry | Yes | Yes | Yes |
| High-priority cases executed | Exit | 100% | 91/91 | Yes |
| All planned cases executed | Exit | ≥ 90% | 100% | Yes |
| Every failed case linked to a defect | Exit | 100% | 100% | Yes |
| helpers.py branch / app.py statement coverage | Exit | ≥ 90% / ≥ 70% | 100% / 98.3% | Yes |
| Every feature has an executed test (RTM) | Exit | 100% | 100% | Yes |
| No open Critical defects | **Release** | 0 | 5 | **No** |

All testing exit criteria are met. The release criterion is not met, which supports the verdict that the app is not ready for release.

## 7. Roles, schedule and deliverables
| Project week (course week) | Phase | Lead | Folder |
|---|---|---|---|
| 1 (4) | Application analysis, black-box | Member 2 (Nurul Afiqah) | /01_Black_Box |
| 2 (5) | White-box and coverage | Member 3 (Shervona) | /02_White_Box_Coverage |
| 3 (6) | GUI, compatibility, usability, accessibility | Member 2 (Nurul Afiqah) | /03_Special_Testing |
| 4 (7) | Web and API | Member 3 (Shervona) | /04_Web_API |
| 5 (8) | Security and performance | Member 4 (Nur Syafiqah) | /05_Security_Performance |
| 6 (9) | Automation and regression | Member 3 (Shervona) | /06_Automation_Regression |
| 7 (10) | Test plan v2, RTM, defect consolidation | Members 1, 2 | /07_Test_Management |
| 8–9 (11–12) | Metrics, evaluation, standards, presentation | Members 4, 1 | /08, /09 |

All members designed and executed tests in every phase, and no one reviewed only their own work.

## 8. Project risks and contingencies
| Risk | Contingency |
|---|---|
| Missed deadlines | Weekly check-in; the support member takes over |
| Results differ between machines | Injected dates; environment recorded |
| Blocking defect (DEF-008) | Fresh database per test |
| Inconsistent IDs across artefacts | One catalogue; `build_documents.py` regenerates everything |
| Live demo fails | Recorded backup video (09_Presentation) |

## 9. Test Strategy
**Risk-based.** Product risks were rated in Week 1 and re-rated as evidence arrived. The Week 1 ratings were too optimistic about security and validation.

| ID | Product risk | L Wk 1 | Impact | Score Wk 1 | L final | Score final | Evidence |
|---|---|---|---|---|---|---|---|
| R-01 | Users can change or delete other users' data | 2 | 3 | 6 | 3 | 9 | DEF-005, 014, 015 |
| R-02 | Injected input changes SQL queries | 2 | 3 | 6 | 3 | 9 | DEF-006 |
| R-03 | Scripts run in other users' browsers | 2 | 3 | 6 | 3 | 9 | DEF-007 |
| R-04 | Bad input corrupts data and crashes pages | 2 | 3 | 6 | 3 | 9 | DEF-008, 009, 018 |
| R-05 | Wrong urgency misleads users | 2 | 2 | 4 | 3 | 6 | DEF-001, 003 |
| R-06 | Valid users cannot register or log in | 2 | 2 | 4 | 3 | 6 | DEF-002, 004 |
| R-07 | Accounts taken over by guessing or stolen cookies | 1 | 3 | 3 | 2 | 6 | DEF-019, 020 |
| R-08 | People with disabilities cannot use the forms | 1 | 2 | 2 | 3 | 6 | DEF-021, 022, 023 |
| R-09 | Slow response at busy times | 1 | 2 | 2 | 1 | 2 | DEF-026 |
| R-10 | Untested browsers behave differently | 2 | 1 | 2 | 1 | 1 | Chrome, Edge, Firefox tested; Safari out of scope |

- **Levels:** unit (helpers.py) → integration/API (Flask client) → system (Selenium, manual GUI) → acceptance-style scenarios. A static code review found the root cause of eight defects before dynamic tests confirmed them.
- **Techniques:** EP, BVA, decision tables, state transitions, basis paths, API negative testing, STRIDE, load testing, WCAG and LEMES reviews.
- **Automation:** test pyramid; automate tests that are repeated, stable, critical and valuable for regression.
- **Defect management:** one central log. Severity (Critical/Major/Moderate/Minor) describes impact; priority (High/Medium/Low) describes urgency. Lifecycle: New → Confirmed (reproduced by a second member) → [developers] Fixed → Retest → Closed, with Duplicate/Rejected/Deferred exits.
- **Metrics:** execution rate, pass rate, automation rate, defects by severity and area, defect density, coverage (see 08).

| Severity | Meaning in PyTodo Pro | Priority | Meaning |
|---|---|---|---|
| Critical | Other users' data exposed or changed, security breach, data loss | High | Fix before release |
| Major | A main rule wrong with no workaround | Medium | Fix in next release |
| Moderate | Wrong behaviour with a workaround; inconsistent validation | Low | Fix when time allows |
| Minor | Cosmetic, wording, edge-case handling | | |
