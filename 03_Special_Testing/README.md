# 03 – GUI, Compatibility, Usability and Accessibility Testing (Project Week 3)

| Brief deliverable | File |
|---|---|
| **Screenshot evidence** | `week 3 evidence/` – every page at desktop, tablet and phone sizes, captured from the real app |
| GUI testing checklist / results | `PyTodo QA Data Collection (Week 3).xlsx` → *GUI Checklist* (15) · `GUI_Usability_Accessibility_Report.md` §1 |
| Compatibility / configuration matrix | `Compatibility_Matrix.md` · sheet *Compatibility* (5) |
| Usability observations | `GUI_Usability_Accessibility_Report.md` §2 (LEMES heuristic review) |
| Basic accessibility findings | `GUI_Usability_Accessibility_Report.md` §3 · sheet *Accessibility* (11) · `axe_results/` |
| Defects and improvement recommendations | report §4 · DEF-001, 021–025 |
| Screenshots / reproducible evidence | `week 3 evidence/`: Login, Register, My Tasks, New Task and Dashboard at desktop, tablet and phone sizes, plus Edit Task and the DEF-002 register error. All captured from the real app with `tools/capture_evidence.py`; `scripts/capture_screenshots.py` does the same against a live server. |

**Results:** GUI 11/15 pass · Accessibility 6/11 pass · Compatibility 4/4 configurations pass (Chrome/Linux; Chrome, Edge and Firefox on Windows 11). Phone layout fails in all (DEF-023). Safari is out of scope (no Mac).

```bash
cd app && python app.py            # terminal 1
python 03_Special_Testing/scripts/capture_screenshots.py     # 18 screenshots (6 pages x 3 sizes)
npm install axe-core && cp node_modules/axe-core/axe.min.js 03_Special_Testing/scripts/
python 03_Special_Testing/scripts/axe_scan.py                # WCAG 2.1 A/AA
```
