# Web and API Test Scenarios

## 1. Main web workflows (covered by black-box and Selenium suites)

| ID | Scenario | Steps | Covered by |
|---|---|---|---|
| WS-01 | New user onboarding | Register → land on My Tasks → empty state | TC-BB-002, AT-001 |
| WS-02 | Daily task management | Log in → create → complete → reopen → edit → delete | TC-BB-021, 032–034, 047, AT-005, AT-006 |
| WS-03 | Finding tasks | Filter by category / status → search → combined | TC-BB-039–044, AT-007 |
| WS-04 | Deadline overview | Tasks due −1/0/1/2/3 days → badges → dashboard counters | TC-BB-025–031, 045–046, AT-004, AT-009 |
| WS-05 | Session security | Log out → protected page → redirect | TC-BB-037–038, AT-003 |
| WS-06 | Client vs server validation | Same bad input via browser and via direct request | §4 below |

## 2. REST endpoints and test types

| Endpoint | Auth | Test types | Tests |
|---|---|---|---|
| POST /api/register | No | Valid, invalid, wrong type, duplicate | TC-API-001–006 |
| POST /api/login | No | Valid, wrong password, unknown user | TC-API-007–009 |
| GET /api/categories | Yes | Functional, no session | TC-API-011–012 |
| GET /api/tasks | Yes | Pagination, filters, search, edge cases | TC-API-010, 025–033 |
| POST /api/tasks | Yes | Valid, missing, wrong type, invalid date, edge | TC-API-013–021 |
| GET / PUT /api/tasks/{id} | Yes | Own, unknown, other user, partial, wrong type | TC-API-022–024, 034–039 |
| DELETE /api/tasks/{id} | Yes | Own, unknown, other user, no session | TC-API-040–043 |
| GET /api/dashboard | Yes | Counts, boundary, no session | TC-API-044–046 |

## 3. Failed API tests – expected vs actual

| ID | Objective | Expected | Actual | Defect |
|---|---|---|---|---|
| TC-API-005 | Duplicate username rejected | 400/409 | 201 `{'id': 2, 'username': 'api_dup'}` | DEF-004 |
| TC-API-006 | Number as username | 400 | 500 | DEF-018 |
| TC-API-011 | Categories need login | 401 | 200 + list | DEF-016 |
| TC-API-016 | Number as title | 400 or 201 "123" | 500 | DEF-018 |
| TC-API-017 | Impossible date | 400 | 500 | DEF-008 |
| TC-API-018 | Wrong date format | 400 | 500 | DEF-008 |
| TC-API-019 | Unknown category id | 400 | 201, category None | DEF-011 |
| TC-API-020 | Non-JSON body | 400/415 "must be JSON" | 400 "title is required" | DEF-017 |
| TC-API-021 | Very long title | 400 | 201 | DEF-013 |
| TC-API-027 | page = −1 | 400 | 200 with tasks | DEF-012 |
| TC-API-028 | per_page = 0 | 400 | 200 [] | DEF-012 |
| TC-API-033 | Apostrophe search | 200 + task | 500 | DEF-006 |
| TC-API-035 | PUT empty title | 400 | 200, title '' | DEF-009 |
| TC-API-036 | done = "false" (string) | 400 / stays open | 200, done = true | DEF-010 |
| TC-API-039 | PUT impossible date | 400 | 500 | DEF-008 |
| TC-API-041 | Delete unknown id | 404 | 200 `{'result': 'ok'}` | DEF-005 |
| TC-API-042 | Delete another user's task | 404/403 | 200; task deleted | DEF-005 |
| TC-API-045 | Due today not overdue | overdue 0 | overdue 1 | DEF-001 |

Happy-path tests all pass, as do 401 for no session and 404 for other users' tasks on GET and PUT. Most failures are negative tests.

## 4. Client-side vs server-side behaviour

Client-side validation helps usability; server-side validation provides security. We sent the same data through the browser and directly to the server:

| Input | Browser | Server / API | Defect |
|---|---|---|---|
| Empty title | Blocked by `required` | Saved by form post and API PUT | DEF-009 |
| Impossible date | Date picker prevents it | Saved, then 500 on every list | DEF-008 |
| Apostrophe in search | Web search works | API search returns 500 | DEF-006 |
| Delete another user's task | Not possible | Possible | DEF-005 |
| Duplicate username | Accepted | Accepted | DEF-004 |

The developer relied on browser checks, or wrote the web and API versions of a feature differently. Anyone using Postman or an edited request skips every client-side check.
