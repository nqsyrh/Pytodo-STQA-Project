# Black-Box Test Design and Justification

Black-box testing derives tests from the requirements without looking at the code. We chose each technique to suit the input:

| Technique | Applied to | Why this technique |
|---|---|---|
| Equivalence Partitioning (EP) | username/password/title/date/search classes | large input domains → one representative per class |
| 3-value BVA | username length, password length, days-until-due | off-by-one errors cluster at edges; 3-value is stricter than 2-value |
| Decision table | registration (3 conditions), login (2 conditions) | outcome depends on combinations of conditions |
| State transition | task Open/Done/Deleted, session Logged-out/Logged-in | features with meaningful states and invalid transitions |

## 1. Equivalence partitions

| Input | Valid classes | Invalid classes | Test cases |
|---|---|---|---|
| Username length / characters | 3–20; letters, digits, `_` | < 3; > 20; space; symbol | TC-BB-001–008 |
| Password length | ≥ 8 | < 8; empty | TC-BB-009–012 |
| Task title | text; special characters | empty; spaces only | TC-BB-021–024, 048 |
| Due date | valid date; none | impossible date (2026-13-45) | TC-BB-021, 022, 049 |
| Search text | partial match; no match; apostrophe | – | TC-BB-041, 042, 044 |

## 2. Boundary value analysis (3-value)

| Step | Username length | Password length | Days until due date |
|---|---|---|---|
| Partitions | 0–2 \| 3–20 \| 21+ | 0–7 \| 8+ | ≤ −1 \| 0 \| 1–2 \| 3+ |
| Boundaries | 3 and 20 | 8 | 0, 1, 2, 3 |
| Coverage items | 2, 3, 4, 19, 20, 21 | 7, 8, 9 | −1, 0, 1, 2, 3 |
| Test cases | TC-BB-001–006 | TC-BB-009–011 | TC-BB-025–029 |
| Result | All pass | 8 fails (DEF-002) | Day 0 fails (DEF-001) |

BVA found two defects that EP alone could miss. In both, the value just inside the valid range failed: the classic off-by-one error.

## 3. Decision table – registration (2³ = 8 rules, simplified to 4)

| Conditions / action | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| C1 Username valid | Y | Y | Y | N |
| C2 Password valid | Y | Y | N | – |
| C3 Username not taken | Y | N | – | – |
| Expected action | Create account | "Username taken" | Password error | Username error |
| Test / result | TC-BB-013 Pass | TC-BB-014 **Fail** (DEF-004) | TC-BB-015 Pass | TC-BB-016 Pass |

When the username is invalid, the other conditions do not matter (don't-care "–"). R2 failed because the system has no action for a taken username, so a duplicate account is created. TC-BB-020 showed that the duplicate account can never log in.

Login (user exists × password correct → 3 rules): TC-BB-017–019, all pass.

## 4. State transitions

| State | Toggle | Delete | Edit | Tests |
|---|---|---|---|---|
| Open | → Done; set `completed_at` | → Deleted | → Open | TC-BB-032, 034, 047 |
| Done | → Open; clear `completed_at` | → Deleted | → Done | TC-BB-033 |
| Deleted | – (refused) | – | – (refused) | TC-BB-035, 036 |

Session: Logged out → protected page → redirect to login (TC-BB-037); Logged in → logout → protected page → redirect (TC-BB-038). All transitions passed, including invalid ones, which were refused safely.

## 5. Test data and justification

- Dates are calculated from the run date (today −1 … today +3), so tests give the same result on any day.
- Some cases post form data directly (title of spaces, date `2026-13-45`) to bypass browser checks and test the server.
- Two users (`qa_user1`, `qa_user2`) allow cross-user checks. Boundary usernames and passwords come from the BVA table.
- The setup password `Passw0rd!` has 9 characters, so DEF-002 does not block other tests.
- Dashboard seed (TC-BB-045): 1 overdue, 1 due soon, 1 upcoming, 1 without a date, 1 completed today → Total 5, Open 4, Overdue 1, Due Soon 1, Completed 1.

## 6. Failed black-box cases

| ID | Technique | Expected | Actual | Defect |
|---|---|---|---|---|
| TC-BB-010 | BVA | Account created | 8-character password refused | DEF-002 |
| TC-BB-014 | DT R2 | "Username taken" | Duplicate registered (302 to /) | DEF-004 |
| TC-BB-020 | DT (from R2) | Second account refused or can log in | Created, cannot log in | DEF-004 |
| TC-BB-023 | EP invalid | No task with blank title | Blank task created | DEF-009 |
| TC-BB-024 | EP valid special chars | Full text shown | `<urgent>` treated as HTML | DEF-007 |
| TC-BB-026 | BVA day 0 | "Due Today" | "Overdue" | DEF-001 |
| TC-BB-046 | BVA day 0 | Overdue 0 | Overdue 1 | DEF-001 |
| TC-BB-048 | EP invalid | Old title kept | Title set to '' | DEF-009 |
| TC-BB-049 | EP invalid date | Date error; list loads | Saved; My Tasks HTTP 500 | DEF-008 |

Failures cluster at boundaries and in server-side validation. This matches the defect-clustering principle (ISTQB, 2023).
