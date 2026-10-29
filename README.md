# gstack SDD kit (ENGR 5520G, Group 6)

Demo is Monday Nov 2. This kit has everything except the two live runs and the final numbers.

## What is in here

| File | Purpose |
|---|---|
| `task/TASK.md` | The toy task text. Paste it unchanged into BOTH runs |
| `task/ANSWER_KEY.md` | Product owner answers. Reveal only when the agent asks |
| `task/tests/` | 30 hidden acceptance tests (10 stated, 20 edge). Do not show the agent |
| `task/reference/lifecycle.py` | Reference solution that proves the tests are right. Never show the agent |
| `score.sh` | `./score.sh <folder with lifecycle.py>` prints stated and edge scores |
| `runs/RUN_A_prompt_engineering.md` | Step by step for the baseline run |
| `runs/RUN_B_gstack.md` | Step by step for the gstack run, with the install command |
| `runs/RESULTS_LOG.md` | Fill this in while you run. It feeds slide 12 |

The presentation deck is a separate Claude artifact (14 slides with speaker notes).

## Schedule

| When | Who | What |
|---|---|---|
| Thu night | Cris | Install gstack, check slash commands appear. Create two throwaway private GitHub repos |
| Thu night | Rohan, Mikhail | Read slides 1 to 10 and their speaker notes. Split who presents which slide |
| Fri | Rohan | Run A (30 min box), log in RESULTS_LOG.md, run `score.sh` |
| Sat | Cris + Mikhail | Run B (gstack sprint), log, run `score.sh`. Screen record the whole run as the demo backup |
| Sun | All | Fill slide 12 and the bracketed sentence on slide 14. Rehearse the 8 minute demo twice |
| Mon Nov 2 | All | Live demo. Keep the recording ready |

## Rules for a fair comparison

1. Same task text, same answer key, same time box (30 min), same model.
2. Nobody edits code by hand. Nobody shows the agent the tests.
3. Run A with gstack switched off (see RUN_A file), Run B with it on.
4. Log every question the agent asks. Those are the "human involvement" evidence.
5. Run B goes second, so the team knows the task better. Say this on slide 14. To reduce the effect,
   have a different person drive each run.

## Verified before handing over

- The 30 tests pass against the reference solution (10 stated, 20 edge).
- A naive implementation passes all 10 stated tests but only 9 of 20 edge tests, so the tests do separate careful work from careless work.
- Not verified: the live gstack install and runs themselves. Those happen on your machines.
# sdd
