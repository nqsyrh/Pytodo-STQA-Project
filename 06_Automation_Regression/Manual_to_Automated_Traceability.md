# Manual-to-Automated Traceability

UI scripts (Selenium, Page Object Model) mapped to the manual cases they automate. The 137 non-UI automated tests keep the SAME IDs as their manual design (e.g. `test_tc_bb_010` automates TC-BB-010), so they are traced one-to-one.

| Script | What it automates | Manual test(s) | Requirement | Result | Defect |
|---|---|---|---|---|---|
| AT-001 | Register and land on My Tasks | TC-BB-002, TC-BB-013 | F01 | Pass |  |
| AT-002 | 8-character password accepted | TC-BB-010 | F01 | Fail | DEF-002 |
| AT-003 | Login, logout, protected page | TC-BB-017, TC-BB-038 | F02 | Pass |  |
| AT-004 | Due-today badge | TC-BB-026 | F10 | Fail | DEF-001 |
| AT-005 | Complete and reopen | TC-BB-032, TC-BB-033 | F07 | Pass |  |
| AT-006 | Delete with confirm dialog | TC-BB-034, TC-GUI-007 | F08 | Pass |  |
| AT-007 | Category filter | TC-BB-039 | F09 | Pass |  |
| AT-008 | HTML in title not rendered | TC-BB-024, TC-SEC-012 | F04 | Fail | DEF-007 |
| AT-009 | Dashboard counters | TC-BB-045 | F11 | Pass |  |
| AT-010 | Browser blocks empty title | TC-GUI-006 | NF3 | Pass |  |

## Automated vs manual by phase

| Phase | Automated | Manual | Script / location |
|---|---|---|---|
| Black-box (Wk 1) | 49 | 0 | 01_Black_Box/test_black_box.py |
| White-box (Wk 2) | 29 | 0 | 02_White_Box_Coverage/test_helpers_unit.py |
| GUI & config (Wk 3) | 0 | 15 | 03_Special_Testing (manual checklist) |
| Accessibility (Wk 3) | 0 | 11 | 03_Special_Testing (Axe + manual) |
| Compatibility (Wk 3) | 0 | 4 | 03_Special_Testing (manual) |
| Web & API (Wk 4) | 46 | 0 | 04_Web_API/test_api.py |
| Security (Wk 5) | 13 | 1 | 05_Security_Performance/test_security.py |
| Performance (Wk 5) | 0 | 5 | 05_Security_Performance/performance/locustfile.py |
| UI automation (Wk 6) | 10 | 0 | 06_Automation_Regression/test_ui_selenium.py |
