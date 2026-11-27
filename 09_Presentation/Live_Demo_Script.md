# Live Demonstration Script (≈ 5 minutes)

**Before the session:** laptop charged; `pip install -r ...` done; app copied into `app/`; Chrome installed; a backup screen recording of this script saved locally (`demo_backup.mp4`).

| Time | Action | Command / click | What the audience sees | Say |
|---|---|---|---|---|
| 0:00 | Start the app | `cd app && python app.py` | Flask running on :5000 | "Unmodified copy, debug as supplied" |
| 0:20 | Show the defect in the UI | Register, create a task due **today** | Red **Overdue** badge | "Boundary defect DEF-001, found by BVA day 0" |
| 1:00 | Run the unit tests | `pytest -m unit -q` | 26 pass, 3 fail | "100% branch coverage, yet 3 failures: coverage is not correctness" |
| 1:40 | Run the API + security suite | `pytest 04_Web_API 05_Security_Performance -q` | 34 pass, 25 fail | "Each failure is tagged with its DEF id" |
| 2:30 | Zoom on one critical test | `pytest -k "tc_api_042" -v` | qa_user1 deletes qa_user2's task | "DEF-005, Critical: any user can delete anyone's task" |
| 3:10 | Selenium | `HEADLESS=0 pytest -m ui -k "at_001 or at_004"` | Browser drives itself; AT-004 fails | "Page Object Model; same defect seen end-to-end" |
| 4:00 | Traceability | Open `07_Test_Management/PyTodo_Test_Management.xlsx` → RTM, then the Metrics sheet | Live formulas | "One catalogue feeds every artefact" |
| 4:40 | CI | Show `.github/workflows/qa.yml` / Actions tab | Pipeline stages | "Bandit would have caught the secret and the SQL" |

**If something fails live:** switch to `demo_backup.mp4` at the same timestamp. Do not debug on stage.
