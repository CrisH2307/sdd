# Results log: prompt engineering vs gstack

Task: vehicle lifecycle tracker (task/TASK.md). Same text, same hidden tests, same answer key.
Run by: ____________   Date: ______   Model: ____________   Claude Code version: ________

| Metric | Run A: prompt engineering | Run B: gstack |
|---|---|---|
| Total minutes | | |
| Prompts / commands we typed | | |
| Questions the agent asked us | | |
| Questions NOT in the answer key (real ambiguity found) | | |
| Hidden tests, stated (x / 10) | | |
| Hidden tests, edge (x / 20) | | |
| Lines of code (lifecycle.py) | | |
| Lines of tests (test_lifecycle.py) | | |
| Manual code edits by us | 0 | 0 |
| Written artifacts produced (spec, plan, review, QA report) | | |
| Human approval points | | |
| Review caught a real defect? (describe) | n/a | |
| Friction / problems | | |

## Run A notes

- Prompt 1 (paste exactly):
- Refinements (one line each):
- Where the agent guessed instead of asking:

## Run B notes

- Questions asked by /spec (list):
- Questions asked by /plan-eng-review (list):
- /review Step 1.5 Scope Drift output (paste or summarize):
- /qa output (summarize):
- What the spec phase surfaced that Run A never asked:

## Honest limits (put these on a slide)

- n = 1 run each, one model, one small task. This is an illustration, not a benchmark.
- Run B came second, so the team knew the task better. Mitigation: ______________
- gstack is a role-based sprint, not a pure spec-driven tool. Its spec step is `/spec`.
