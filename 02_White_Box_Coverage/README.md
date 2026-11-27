# 02 – White-Box Testing and Coverage (Project Week 2)

| Brief deliverable | File |
|---|---|
| **Screenshot evidence, one per test** | `week 2 evidence/` – 29 test cards + `run_pytest_unit.png` + `run_statement_coverage.png` |
| Selected code units and justification | `White_Box_Analysis.md` §1 |
| Control-flow analysis | `White_Box_Analysis.md` §2, `figures/cfg_compute_urgency.png` |
| White-box test cases | `PyTodo QA Data Collection (Week 2).xlsx` (29) |
| Automated / unit test file | `test_helpers_unit.py` |
| Coverage report and interpretation | `coverage_html/` (generated) + `White_Box_Analysis.md` §4 |

**Result:** 29 executed, 26 pass, 3 fail (DEF-001, DEF-002, DEF-003).

```bash
pytest 02_White_Box_Coverage -v
pytest -m "not ui" --cov=app --cov=helpers --cov-branch --cov-report=term-missing \
       --cov-report=html:02_White_Box_Coverage/coverage_html
```
