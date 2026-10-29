# Run A: prompt engineering (plain Claude Code, no gstack)

Goal: get the best result you can by writing and refining prompts. This is the baseline.
Time box: 30 minutes. Start a stopwatch. One person drives, one person logs.

## Setup (5 min)

```bash
mkdir -p ~/sdd-demo/run-a && cd ~/sdd-demo/run-a && git init
```

Use a Claude Code session WITHOUT gstack active. Easiest way: a fresh machine user or
temporarily move the folder: `mv ~/.claude/skills/gstack ~/.claude/skills/gstack.off`
(restore it before Run B: `mv ~/.claude/skills/gstack.off ~/.claude/skills/gstack`).
Check by typing `/` in Claude Code: no gstack commands should appear.

## Procedure

1. Paste the full text of `task/TASK.md` as your first message, plus ONE sentence of
   your own prompt engineering (role, output format, "write tests first", etc.).
   Save that prompt in RESULTS_LOG.md as Prompt 1.
2. Let Claude work. If it asks a question, answer from `task/ANSWER_KEY.md` (verbatim).
   If the question is not in the answer key, answer "your call" and log it.
3. You may refine the prompt as many times as you like. Log each refinement and count it.
   Rules: never paste the answer key or hidden tests proactively; never edit code by hand.
4. Stop when you are happy or at 30 minutes, whichever comes first.
5. Score it: `./score.sh ~/sdd-demo/run-a`
6. Copy the log into RESULTS_LOG.md (Run A column). Screenshot the final test output.

## What to record

- Number of prompts you sent (first + refinements)
- Questions the agent asked, and your answers
- Minutes from first prompt to "done"
- Score output: stated x/10, edge x/20
- Lines of code and lines of tests
- Anything you had to correct by hand (should be nothing)
- One observation: where did the agent guess instead of ask?
