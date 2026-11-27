# Compatibility and Configuration Matrix

**Scope:** testing every OS × browser × screen combination is impossible, so we tested the browsers our group actually uses: **Chrome, Edge and Firefox**, each at desktop, tablet and phone size. **Safari / macOS is out of scope** because no member owns a Mac; it is recorded as residual risk R-10 and as future testing.

| Browser / OS | Desktop 1366×768 | Tablet 768×1024 | Phone 375×812 | Test case | Where / when |
|---|---|---|---|---|---|
| Chrome 153 / Linux | Pass | Pass | **Fail** (DEF-023) | TC-COMP-001, TC-GUI-012–014 | Cloud verification run, 27 Nov 2026 |
| Chrome 158.0.8127.89 / Windows 11 | Pass | Pass | **Fail** (DEF-023) | TC-COMP-002 | Member laptop, 27 Nov 2026 (`run_browser_tests.bat chrome`) |
| Edge 158.0.4370.33 / Windows 11 | Pass | Pass | **Fail** (DEF-023) | TC-COMP-003 | Member laptop, 27 Nov 2026 (`run_browser_tests.bat edge`) |
| Firefox 161.0 / Windows 11 | Pass | Pass | **Fail** (DEF-023) | TC-COMP-004 | Member laptop, 27 Nov 2026 (`run_browser_tests.bat firefox`) |

**Result: 4 of 4 configurations pass the smoke set** (register, login, create, complete, filter, dashboard, logout). The phone layout fails in every browser.

## Selenium suite (10 tests) per browser

| Browser | Passed | Failed | Failing tests | Note |
|---|---|---|---|---|
| Chrome 158 / Windows | 7 | 3 | AT-002 (DEF-002), AT-004 (DEF-001), AT-008 (DEF-007) | AT-005 hit a Selenium timing error once, then passed on re-run |
| Edge 158 / Windows | 7 | 3 | same | AT-003 hit a timing error once, then passed on re-run |
| Firefox 161 / Windows | 7 | 3 | same | – |

The defects are the same in every browser, which shows they are in the application, not the browser. The two one-off timing errors are flaky tests, not application defects; they are noted in the automation reflection. Run summaries: `06_Automation_Regression/week 6 evidence/*_run_summary.txt`.

## Phone layout (DEF-023), observed two ways

- **Narrow window** (Chrome on Linux at 375 px, Firefox on Windows): the task table is wider than the window, so users must scroll sideways and the Urgency column and Delete link are cut off.
- **Device emulation** (Chrome and Edge on Windows): the browser shrinks the whole desktop page to fit, because the app has no `<meta name="viewport">`, so the text is unreadably small.

Either way the page is not usable on a phone, a WCAG 1.4.10 Reflow failure. Evidence: `week 3 evidence/<browser>/index_phone.png` and `index_desktop.png`. The desktop screenshots also show the due-today task labelled Overdue (DEF-001).

## Re-running a browser

On a Windows laptop with the repo, open Command Prompt in the repo root and run `run_browser_tests.bat chrome`, `edge` or `firefox`. It installs the requirements, starts the app, runs the 10 Selenium tests, captures every page at three sizes with a layout check (`week 3 evidence/<browser>/compatibility_result.json`), and writes the exact browser version to `reports/browser_<browser>.txt`.
