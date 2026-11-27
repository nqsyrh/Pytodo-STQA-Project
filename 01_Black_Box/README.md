# 01 – Application Analysis and Black-Box Testing (Project Week 1)

| Brief deliverable | File |
|---|---|
| **Screenshot evidence, one per test** | `week 1 evidence/` – 49 cards from the real app (`TC-BB-xxx_PASS.png` / `_FAIL.png`): request/response, the page the app rendered, and the test code |
| Application overview and feature inventory | `Feature_Inventory_and_Risk_Matrix.md` §1–2 |
| Initial test scope / risk matrix | `Feature_Inventory_and_Risk_Matrix.md` §3 |
| Black-box test scenarios and cases | `PyTodo QA Data Collection (Week 1).xlsx` (49 cases, full Test Case Template) |
| Test data and technique justification | `Black_Box_Test_Design.md` |
| Execution evidence | `test_black_box.py` → `reports/junit_all.xml`, `reports/pytest_all.log`; browser confirmation by Selenium (06) |
| Initial defect records | `../07_Test_Management/Defect_Reports.md` (DEF-001, 002, 004, 007, 008, 009) |

**Result:** 49 executed, 40 pass, 9 fail (81.6%).

**Execution note:** the cases were run through the web forms as HTTP form submissions, scripted with the Flask test client so that they can be repeated identically on any day. Key results were also confirmed in a real browser with Selenium (folder 06). Cases that post data directly (title of spaces, date `2026-13-45`) bypass the browser's own checks on purpose, so they test the server.

**Why scripted instead of clicked by hand:** each case is scripted so it can be re-run identically after every fix. Clicking by hand cannot bypass the browser's own checks, which TC-BB-023, 048 and 049 need. The same scripts then serve as the Week 6 regression suite. Key results were confirmed visually on the real app (`../03_Special_Testing/week 3 evidence/`).

Run: `pytest 01_Black_Box -v`
