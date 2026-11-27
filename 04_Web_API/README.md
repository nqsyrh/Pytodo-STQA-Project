# 04 – Web and API Testing (Project Week 4)

| Brief deliverable | File |
|---|---|
| **Screenshot evidence, one per test** | `week 4 evidence/` – 46 cards showing each request, status code and JSON response |
| Web test scenarios | `Web_Test_Scenarios.md` §1 |
| API test suite | `test_api.py` (46 tests) |
| Request / test data | `api_request_data.json` (generated), `PyTodo QA Data Collection (Week 4).xlsx` |
| Expected vs actual status / response | `PyTodo QA Data Collection (Week 4).xlsx`, `Web_Test_Scenarios.md` §3 |
| Execution evidence and defects | `reports/junit_all.xml`; DEF-001, 004–006, 008–013, 016–018 |

**Result:** 46 executed, 28 pass, 18 fail (60.9%). Rule: a 5xx answer to client input always counts as a failure, because the server must answer with 4xx.

Run: `pytest 04_Web_API -v`
