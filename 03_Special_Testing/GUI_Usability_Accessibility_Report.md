# GUI, Usability and Accessibility Report

Environment: Chrome 153 on Linux, desktop 1366×768, tablet 768×1024, phone 375×812. Every page of the app (Login, Register, My Tasks, New Task, Edit Task, Dashboard) was opened in Chrome at the three sizes and screenshotted (`week 3 evidence/`). axe-core checked WCAG 2.1 A and AA rules. We then checked the keyboard by hand and reviewed each screen against the checklist.

## 1. GUI checklist (15 checks: 11 pass, 4 fail)

Titles, navigation, button labels, error messages, required-field checks, delete confirmation, done-task styling and empty-state messages all work.

| ID | Check | Actual | Defect |
|---|---|---|---|
| TC-GUI-008 | Each urgency label has its own badge style | "Due Today" never appears; a task due today shows red "Overdue" | DEF-001 |
| TC-GUI-011 | Confirmation after create / edit / delete | No message; page silently reloads | DEF-024 |
| TC-GUI-014 | Layout at phone 375×812 | Task list, New Task and Dashboard scroll sideways; Urgency column cut off; username cut off | DEF-023 |
| TC-GUI-015 | Form keeps typed values after a validation error | Both fields are emptied | DEF-025 |

![Desktop: task due today shows Overdue (DEF-001), HTML title rendered bold (DEF-007)](week%203%20evidence/my_tasks_desktop.png)

![Phone layout: Urgency column cut off (DEF-023)](week%203%20evidence/my_tasks_phone.png)

## 2. Usability – heuristic review (LEMES)

This is an expert walkthrough by the team, not testing with real users.

| Dimension | Positive | Issue |
|---|---|---|
| Learnability | Simple layout; first task created in under a minute | The page says 8 characters, but 9 are enforced (DEF-002) |
| Efficiency | Dropdown filters apply instantly | Search needs the Filter button (inconsistent); no sort by due date |
| Memorability | Same top bar and styles on every page | – |
| Errors | Delete confirmation; plain-language errors | No success messages (DEF-024); register form clears input (DEF-025); one bad date crashes the list (DEF-008) |
| Satisfaction | Clean look; badges use text and colour | Phone layout needs sideways scrolling (DEF-023) |

## 3. Accessibility (WCAG 2.1 – 11 checks: 6 pass, 5 fail)

Pass: language of page, page titles, keyboard order, visible focus, text error messages, urgency not conveyed by colour alone.

| ID | WCAG criterion | Actual | Defect |
|---|---|---|---|
| TC-ACC-003 | 1.3.1 / 4.1.2 (A) Labels | axe `label` (critical): 2 inputs on Login, 2 on Register, 3 on New Task; `<label>` not linked to its input | DEF-021 |
| TC-ACC-004 | 4.1.2 (A) Name, role, value | axe `select-name` (critical): category and status `<select>` have no name | DEF-021 |
| TC-ACC-005 | 1.4.3 (AA) Contrast | Empty-state text #999 on white = 2.8:1 (also done-task titles) | DEF-022 |
| TC-ACC-010 | 1.4.10 (AA) Reflow | Horizontal scroll; Urgency column hidden | DEF-023 |
| TC-ACC-011 | 4.1.2 / 2.4.6 Button names | Button text is only the symbol ○ or ✓; a screen reader says "white circle" | DEF-021 |

**POUR summary:** the app is operable and understandable, but weak on *perceivable* (contrast) and *robust* (labels are not linked to inputs, so a screen reader cannot name the fields). **It does not reach WCAG 2.1 Level AA.**

## 4. Recommendations

1. Link each `<label for=…>` to its input. Add `aria-label` to the two filter dropdowns and to the ○/✓ button.
2. Darken grey text to at least #767676 (4.5:1).
3. Make the task table responsive: stack its columns on narrow screens.
4. Show success messages after create, edit and delete. Keep typed values after a validation error.
5. Show "Due Today" with its own badge colour once DEF-001 is fixed.
