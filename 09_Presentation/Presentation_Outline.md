# Final Presentation – Slide Plan (about 15 min + 5 min demo)

| # | Slide | Content | Speaker |
|---|---|---|---|
| 1 | Title | PyTodo Pro – Independent QA Evaluation; team, roles | Lead |
| 2 | Verdict first | Not ready for release: 183 tests, all 183 run, 131 pass, 26 defects (5 Critical) | Lead |
| 3 | The app and our scope | 3-tier diagram, 12 features, what was out of scope | Test Design |
| 4 | Risk-based approach | Week 1 risk matrix → final re-rating (security rose to 9) | Lead |
| 5 | Black-box | BVA table; decision table R2; DEF-001/002 off-by-one | Test Design |
| 6 | White-box | CFG, V(G)=5, 100% coverage yet 3 failures → coverage ≠ correctness | Automation |
| 7 | GUI / accessibility | Phone screenshot, WCAG failures, not AA | Test Design |
| 8 | API vs UI | Client-vs-server table: the UI hides what the API allows | Automation |
| 9 | STRIDE + top 3 security findings | Session forgery, SQL injection, cross-user delete | Defects & Metrics |
| 10 | Performance | p95 chart; login bottleneck; limitations | Defects & Metrics |
| 11 | Automation & regression | Pyramid, POM, 52-test regression suite, reflection | Automation |
| 12 | Metrics | Results by phase, defects by severity/area, defect density caveat | Defects & Metrics |
| 13 | Residual risk & recommendations | Fix-now list; untested areas | Lead |
| 14 | Standards | ISO/IEC 25010 coverage, CI/CD pipeline, ISO 9001 and CMMI (no level claimed) | Lead |
| 15 | Live demo | see `Live_Demo_Script.md` | Automation |
| 16 | Lessons learned + Q&A | Boundaries hide defects; coverage ≠ correctness; test the API directly | All |

Charts for the slides: `../08_Final_QA_Report/charts/`.
