# Standards Integration

## 1. ISO/IEC 25010 characteristics
| Characteristic | How evaluated | Evidence |
|---|---|---|
| Functional suitability | **Directly** – black-box, white-box, API | 01, 02, 04 |
| Security | **Directly** – STRIDE + 14 security tests | 05 |
| Usability (incl. accessibility) | **Directly** – GUI checklist, LEMES, WCAG 2.1 | 03 |
| Performance efficiency | **Directly** – Locust load and stress | 05 |
| Compatibility | **Directly** – Chrome, Edge and Firefox on Windows 11 plus Chrome on Linux, each at three screen sizes; Safari out of scope | 03 |
| Reliability | **Indirectly** – error handling (500s), fault tolerance to bad input | 04, DEF-008/018 |
| Maintainability | **Indirectly** – code review, V(G), testability | 02 |
| Portability | **Not adequately evaluated** – only run locally | – |

Also not adequately evaluated: availability and recoverability, capacity on a real server, and accessibility with real users.

**Other standards:** IEEE 829 shaped our test plan, test case and defect report structure. Our weekly cycle of plan → test → review → adjust mirrors ISO 9001's Plan-Do-Check-Act. **CMMI:** the original development shows no evidence of reviews, standards or automated checks, which is typical of Level 1 (Initial). Our project introduces defined test processes (Level 3 practices) and metrics, a first step toward Level 4 (Quantitatively Managed).

## 2. Regression tests in CI/CD and continuous testing
`.github/workflows/qa.yml` runs cheap checks first and stops the pipeline early:

| Stage | What runs | Gate | Would have caught |
|---|---|---|---|
| Static analysis | Bandit, flake8 | No high findings | Hard-coded secret, f-string SQL, debug=True |
| Unit tests | `pytest -m unit` + coverage | All pass; branch ≥ 90% | DEF-001, 002, 003 |
| API regression | `pytest -m "regression and not ui"` | All pass | DEF-004, 005, 007, 008, 009 |
| UI smoke | Selenium headless | All pass | Broken pages, XSS |
| Nightly | Locust baseline, axe scan | No regression | DEF-021, 026 |

This is continuous testing: every change is checked automatically, a fixed defect cannot quietly return, and testing moves left to the moment code is written, when fixes are cheapest.

## 3. Process improvements for Agile / DevOps
| Improvement | Prevents | Where it fits |
|---|---|---|
| Acceptance criteria with boundary examples in user stories | DEF-001, 002, 003 | Backlog refinement |
| Secure-coding checklist in code review (parameterised SQL, ownership checks, no `\|safe`, no secrets) | DEF-005, 006, 007, 014 | Pull request review |
| One shared server-side validation function for web and API | DEF-008–011, 013, 018 | Definition of Done |
| UNIQUE username, CSRF tokens, rate limiting | DEF-004, 015, 019 | Framework setup |
| Accessibility checklist and axe in CI | DEF-021, 022, 023 | Definition of Done |
