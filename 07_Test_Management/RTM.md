# Requirements Traceability Matrix

Generated from `tools/test_catalogue.py`. Uses the RTM template from the Group Project 2 brief. Every requirement has at least one executed test.

| Requirement/Feature | Test Scenario | Test Case ID(s) | Test Type/Technique | Result | Defect ID |
|---|---|---|---|---|---|
| F01 Registration | Valid/invalid account creation; username & password boundaries; duplicate username | TC-BB-001-016, TC-WB-009-018, TC-API-001-006, TC-SEC-011, AT-001-002 | API, BVA, Decision table, EP, Security (STRIDE), Selenium UI, White-box path/branch | 29/35 passed | DEF-002, DEF-004, DEF-018 |
| F02 Login / logout | Valid/invalid authentication; logout; brute force; session replay | TC-BB-017-020, TC-BB-038, TC-API-007-009, TC-SEC-001, TC-SEC-004-005, AT-003 | API, Decision table, Security (STRIDE), Selenium UI, State transition | 9/12 passed | DEF-004, DEF-019, DEF-020 |
| F03 Access control | Logged-out redirect/401; cross-user GET/PUT/DELETE; cookie forgery | TC-BB-037, TC-API-010, TC-API-024, TC-API-037, TC-API-042, TC-SEC-002-003, TC-SEC-007-009, TC-SEC-014 | API, Security (STRIDE), State transition | 8/11 passed | DEF-005, DEF-014 |
| F04 Create task | Create with valid/invalid title, date, category, types; XSS in title | TC-BB-021-024, TC-BB-049, TC-API-013-021, TC-SEC-013, AT-008 | API, EP, Security (STRIDE), Selenium UI | 5/16 passed | DEF-007, DEF-008, DEF-009, DEF-011, DEF-013, DEF-014, DEF-017, DEF-018 |
| F05 View / list | List order; pagination; get by id; output encoding | TC-API-022-023, TC-API-025-029, TC-SEC-012 | API, Security (STRIDE) | 5/8 passed | DEF-007, DEF-012 |
| F06 Edit task | Edit fields; partial update; empty title; invalid date | TC-BB-036, TC-BB-047-048, TC-API-034-035, TC-API-038-039 | API, EP, State transition | 4/7 passed | DEF-008, DEF-009 |
| F07 Complete / reopen | Complete/reopen state transitions; completed_at; done type | TC-BB-032-033, TC-BB-035, TC-WB-026-029, TC-API-036, AT-005 | API, Selenium UI, State transition, White-box path/branch | 8/9 passed | DEF-010 |
| F08 Delete task | Owner delete; unknown id; CSRF; no session | TC-BB-034, TC-API-040-041, TC-API-043, TC-SEC-006, AT-006 | API, Security (STRIDE), Selenium UI, State transition | 4/6 passed | DEF-005, DEF-015 |
| F09 Filter / search | Category/status filters; partial search; apostrophe; SQL injection | TC-BB-039-044, TC-API-030-033, TC-SEC-010, AT-007 | API, EP, Security (STRIDE), Selenium UI | 10/12 passed | DEF-006 |
| F10 Urgency | Boundary around due-date classification (day -1, 0, 1, 2, 3); none; done | TC-BB-025-031, TC-WB-001-008, AT-004 | BVA, EP, Selenium UI, White-box data-flow, White-box path/branch | 13/16 passed | DEF-001 |
| F11 Dashboard | Dashboard counters; due-today; 7-day completed window | TC-BB-045-046, TC-WB-019-025, TC-API-044-046, AT-009 | API, BVA, EP, Selenium UI, White-box path/branch | 10/13 passed | DEF-001, DEF-003 |
| F12 Categories | Category list with/without session | TC-API-011-012 | API | 1/2 passed | DEF-016 |
| NF2 Performance | Response time, throughput, errors at 1/10/25/50/100 users | TC-PERF-001-005 | Load/stress | 3/5 passed | DEF-026 |
| NF3 GUI / usability | Checklist of forms, buttons, messages, navigation, feedback | TC-GUI-001-011, TC-GUI-015, AT-010 | GUI checklist, Selenium UI | 10/13 passed | DEF-001, DEF-024, DEF-025 |
| NF4 Accessibility | WCAG 2.1 A/AA checks with axe-core and keyboard | TC-ACC-001-011 | WCAG review | 6/11 passed | DEF-021, DEF-022, DEF-023 |
| NF5 Compatibility | Chrome, Edge, Firefox (Windows) and Chrome (Linux) x 3 viewports; smoke set | TC-GUI-012-014, TC-COMP-001-004 | Compatibility, Configuration | 6/7 passed | DEF-023 |
