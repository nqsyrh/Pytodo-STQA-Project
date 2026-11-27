# Automation Candidates, Approach and Reflection

## 1. Which tests we automated and why

We reviewed every manual test from Weeks 1–5 against four criteria: **repetition** (run on every change), **stability** (expected result does not change), **criticality** (high-risk feature) and **regression value** (likely to break again).

| Candidate group | Repetition | Stable | Critical | Regression value | Decision |
|---|---|---|---|---|---|
| BVA / EP on registration and urgency | High | Yes | Yes | Every failed boundary | Automate (PyTest) |
| helpers.py rules | High | Yes | Yes | Yes | Automate (unit) |
| API happy and negative paths | High | Yes | Yes | Yes | Automate (Flask client) |
| Cross-user / injection / XSS checks | Medium | Yes | Critical | Yes | Automate (security) |
| Main UI journeys | Medium | Mostly | Yes | Yes | Automate 10 (Selenium, POM) |
| Look and feel, usability judgement | Low | No | – | – | Manual |
| WCAG judgement (contrast, screen reader) | Low | – | – | – | Manual + axe |
| One-off browser checks | Low | – | – | – | Manual smoke |
| Debugger exposure (TC-SEC-013) | Once | – | – | – | Manual (needs browser + debug server) |

**Result:** 147 of 183 cases (80.3%) are automated. The 10 Selenium tests were also run on member laptops in Chrome 158, Edge 158 and Firefox 161 on Windows 11: 7 pass / 3 fail in each, on the same defects.

## 2. Test pyramid

| Layer | Tool | Tests | Run time |
|---|---|---|---|
| UI / end-to-end (few) | Selenium WebDriver + Page Object Model | 10 | ≈ 20 s |
| API / integration | PyTest + Flask test client (forms, API, security) | 108 | ≈ 18 s |
| Unit (many) | PyTest | 29 | < 1 s |

Every test starts with a fresh temporary database, so tests never depend on each other. The Page Object Model keeps all locators in `pages/`, so a renamed button needs one fix in one file. Routes and field names live in `qa_config.py` for the same reason.

## 3. Reflection

**Benefits**
- The 137 non-UI tests run in about 20 seconds, so we re-ran them many times and got identical results.
- Generating spreadsheets, the RTM and metrics from one catalogue and the PyTest results kept IDs and statuses consistent across artefacts.
- The 24 failing regression tests become ready-made confirmation tests once the developers fix the defects.

**Limitations**
- Scripts took longer to write than one manual run, so they pay off only after several runs.
- One Selenium test was flaky until explicit waits were added. Even then, AT-003 (Edge) and AT-005 (Chrome) each hit a one-off timing error on Windows and passed on re-run, which shows that UI tests need re-run rules.
- Automation cannot judge usability or visual quality, and 100% coverage did not mean correct code (DEF-001 to 003 hide inside fully covered code).
- Tests are coupled to routes and field names. `qa_config.py` limits that coupling but cannot remove it.
