# Run B: gstack (spec first, then build, review, QA)

Goal: same task, driven by gstack's sprint. Same time box and same rules as Run A.

## Setup (5 min, do it once tonight)

Requirements: Claude Code, Git, Bun 1.3.3 or newer (gstack's README recommends 1.4.2+).

Open Claude Code and paste:

> Install gstack: run `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup` then add a "gstack" section to CLAUDE.md that says to use the /browse skill from gstack for all web browsing and never use mcp__claude-in-chrome__* tools.

Then, in the demo repo:

```bash
mkdir -p ~/sdd-demo/run-b && cd ~/sdd-demo/run-b && git init
```

Check: type `/` in Claude Code. You should see `/office-hours`, `/spec`, `/plan-eng-review`,
`/review`, `/qa`, `/ship`. If not: `cd ~/.claude/skills/gstack && ./setup`.

Note: `/spec` files its output as a GitHub issue (via `gh`) and always archives a copy locally;
`/ship` opens a PR. So give the demo repo a real remote. Create a throwaway private repo
(`gh auth login` once, then `gh repo create sdd-demo-run-b --private --source=. --push`
after an initial commit). Do the same for Run A if you want equal conditions.
If a step still fails without a remote, log it as friction and say "skip".

## Procedure (the sprint)

| Step | Command | What you do | Artifact to save |
|---|---|---|---|
| 1 Spec | `/spec` then paste `task/TASK.md` | Answer its questions from `task/ANSWER_KEY.md`. Log each question. Approve the Phase 4 draft. | The spec (issue text or local archive) |
| 2 Plan | `/plan-eng-review` | Answer questions, approve the plan | Plan file, test plan, diagrams |
| 3 Build | Exit plan mode, let Claude implement | Do not edit by hand | `lifecycle.py`, `test_lifecycle.py` |
| 4 Review | `/review` | Approve or reject each ASK. Note the Scope Drift check output | Review report |
| 5 Test | `/qa` (CLI mode, no browser needed) | Let it run | QA report |
| 6 Ship | `/ship` only if a git remote exists, else skip | | Test count before/after |

Optional shortcut if time is short: `/autoplan` instead of step 2 (runs the plan reviews in one go).
If `/spec` feels heavy for a toy task, fall back to `/office-hours` for step 1 and log that you did.

## Score and record

1. `./score.sh ~/sdd-demo/run-b`
2. Fill the Run B column in RESULTS_LOG.md.
3. Save every artifact (copy `~/.gstack/` or wherever the skill says it archived, plus screenshots).

## What to record

- Every question gstack asked, and your answer. Count the human decision points.
- Which questions were NOT in the answer key (the agent found a real ambiguity).
- Minutes per step and total
- Score output: stated x/10, edge x/20
- Review findings: did `/review` Step 1.5 (Scope Drift Detection) report MISSING REQUIREMENTS or SCOPE CREEP?
- Friction: install problems, steps that needed a remote, steps that felt too heavy for a toy
- One observation: what did the spec phase surface that Run A never asked?
