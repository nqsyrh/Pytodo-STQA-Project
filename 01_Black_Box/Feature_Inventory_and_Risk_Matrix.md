# Application Overview, Feature Inventory and Initial Risk Matrix

## 1. Application overview

PyTodo Pro lets a registered user create, categorise, search, complete and delete personal tasks with optional due dates. Each task gets an urgency label, and a dashboard summarises them. The same functions are offered as a JSON REST API. There is one user type, and each user must see and change only their own tasks.

| Tier | Technology | Tested by |
|---|---|---|
| Presentation | 6 Jinja2 templates, CSS, HTML5 form validation | GUI, usability, accessibility, compatibility, Selenium |
| Application | Python, Flask 3.0.3; `app.py` 482 lines, `helpers.py` 75 lines; session cookies | Black-box, white-box, API, security |
| Data | SQLite: `users`, `categories`, `tasks` | Data integrity, injection |

**Users:** students and young professionals managing personal deadlines (single role). **Quality expectations (ISO/IEC 25010):** correct urgency and dashboard rules, private tasks, bad input never crashes the app, usable by new users, fast at normal load, works on common browsers and phones.

## 2. Feature inventory (requirements baseline – README and helpers.py)

| ID | Feature | Business rule | Testable conditions |
|---|---|---|---|
| F01 | Registration | Username 3–20 chars (letters, digits, `_`); password ≥ 8 chars | length boundaries, character classes, duplicate username |
| F02 | Login / logout | Correct credentials start a session; logout ends it | valid / wrong password / unknown user; session after logout |
| F03 | Access control | Logged out → redirect or 401; users reach only their own tasks | each protected page / endpoint; cross-user ids |
| F04 | Create task | Title required; category and due date (YYYY-MM-DD) optional | empty / spaces / special chars / long title; invalid date |
| F05 | View / list | Newest first; API pagination (`page`, `per_page`) | order, paging edges |
| F06 | Edit task | Edit fields; API partial update | partial update, invalid values |
| F07 | Complete / reopen | `completed_at` set when done, cleared when reopened | state transitions |
| F08 | Delete task | Only the owner can delete | owner / other user / unknown id |
| F09 | Filter / search | Category and status filters; search on part of the title | partial match, no match, apostrophe |
| F10 | Urgency | No due date, Overdue, Due Today, Due Soon (1–2 days), Upcoming (3+ days), Done | day −1, 0, 1, 2, 3 |
| F11 | Dashboard | Total, Open, Overdue, Due Soon, Completed in last 7 days (inclusive) | counters, 7-day boundary |
| F12 | Categories | Work, Personal, Study, Urgent | list, auth |
| NF2 | Performance | Responsive at expected load | p95, errors |
| NF3 | GUI / usability | Clear, consistent, gives feedback | checklist, LEMES |
| NF4 | Accessibility | WCAG 2.1 AA | axe-core + manual |
| NF5 | Compatibility | Common browsers and screen sizes | browser × OS × viewport |

## 3. Initial test scope and risk matrix (Week 1, before testing)

Risk = likelihood × impact (1–3 each). Highest-risk features were tested first and most deeply (risk-based testing).

| Feature | Likelihood | Impact | Score | Priority | Reason | In scope |
|---|---|---|---|---|---|---|
| F03 Access control / F08 Delete | 2 | 3 | 6 | High | Privacy of every user | Yes – UI + API + STRIDE |
| F04 / F06 input validation | 2 | 3 | 6 | High | Bad data could corrupt tasks | Yes – EP + API negative |
| F09 Search / filter | 2 | 3 | 6 | High | User text reaches database queries | Yes – EP + injection |
| F10 Urgency / F11 Dashboard | 2 | 2 | 4 | Medium | Date boundaries are error-prone | Yes – BVA + white-box |
| F01 Registration / F02 Login | 2 | 2 | 4 | Medium | Gate to the whole app | Yes – BVA + decision table |
| F05 List, F07 Toggle, F12 | 1 | 1–2 | 1–2 | Low | Simple display logic | Yes – state transition, API |

**Out of scope:** changing the code, production hosting, load beyond one machine, uncontrolled penetration testing (forbidden by the brief), testing with real users who have disabilities.

The final re-rated risk register (Week 1 vs final) is in `../07_Test_Management/Test_Plan_and_Strategy.md` §9. The Week 1 ratings were too optimistic about security and validation.
