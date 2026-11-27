# Residual Risk and Overall Quality Assessment

No defect has been fixed, so every confirmed risk remains as residual risk.

## 1. Residual risks
| Risk | Level | Evidence | Recommended action |
|---|---|---|---|
| Users can change or delete other users' data | High | DEF-005, 014, 015 | Scope every query by user_id; remove hard-coded secret; CSRF tokens |
| Injected input changes SQL queries | High | DEF-006 | Parameterised queries everywhere; Bandit in CI |
| Scripts run in other users' browsers | High | DEF-007 | Remove `\|safe`; keep Jinja autoescape |
| Bad input corrupts data and crashes pages | High | DEF-008, 009, 018 | Server-side validation of dates, titles and types |
| Wrong urgency misleads users | High | DEF-001, 003 | Fix boundary conditions; keep BVA tests in regression |
| Valid users cannot register or log in | High | DEF-002, 004 | `>=` 8; UNIQUE username |
| Account takeover by guessing or stolen cookies | High | DEF-019, 020 | Rate limiting; server-side sessions |
| People with disabilities cannot use the forms | High | DEF-021, 022, 023 | Labels, aria-labels, contrast, responsive table |
| Slow response at busy times | Low | DEF-026 | Load test on production-like server |
| Untested browsers behave differently | Low | Safari out of scope | Test Safari / macOS and real phones when available |

**Important untested areas:** Safari (out of scope, no Mac) and real phones; the API `status=open` filter; screen-reader testing with real users; long-running reliability, crash recovery and concurrent edits; production-like performance; automated security scanning.

## 2. Quality by ISO/IEC 25010 characteristic
| Characteristic | Rating | Reason |
|---|---|---|
| Functional suitability | Fair | Main flows correct; urgency and validation boundaries wrong |
| Security | Poor | Cross-user delete, SQL injection, XSS, session forgery |
| Reliability | Poor | One bad date permanently crashes a user's pages; wrong types give 500 |
| Usability | Fair | Easy to learn; weak feedback and phone layout |
| Performance efficiency | Good | Fast at expected load; login slow only in bursts |
| Compatibility | Fair | Chrome, Edge and Firefox desktop/tablet fine; phone layout fails in all |
| Maintainability | Good | Small, readable code; helpers.py easy to test (V(G) ≤ 5) |
| Portability | Not evaluated | Only run locally |

## 3. Overall assessment and limitations
PyTodo Pro is a good prototype with a clean, testable structure. On our evidence, it is **not fit for release** until the Critical and Major defects are fixed and the regression suite passes. Testing shows that defects are present, not that they are absent (ISTQB, 2023), and the untested areas above still carry risk. A 71% pass rate does not mean weak testing: the tests were designed to find defects, many of them on edges and negative cases. The defect density (46.7 per KLOC) looks high because the app is tiny (557 lines) and several defects sit in templates or CSS, so treat it only as a rough indicator.

## 4. Prioritised recommendations and future testing
1. **Fix now (Critical):** scope DELETE by user_id (DEF-005); parameterise search SQL (DEF-006); remove `|safe` (DEF-007); validate input on the server (DEF-008); move SECRET_KEY to an environment variable and turn debug off (DEF-014).
2. **Fix next (Major):** urgency boundary (DEF-001), password `>=` 8 (DEF-002), unique usernames (DEF-004), CSRF tokens (DEF-015), form labels (DEF-021).
3. **Then:** Moderate and Minor defects, starting with DEF-018, 019 and 020. Re-run `pytest -m regression` for confirmation and regression testing.
4. **Future testing:** complete the browser matrix, including Safari; screen-reader testing; a production-like load test; an OWASP ZAP scan in a controlled environment; add the `status=open` API test; refresh tests regularly to avoid the pesticide paradox.
