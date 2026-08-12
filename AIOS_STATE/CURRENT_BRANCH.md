# Current Branch / Stem

## Branch
`phase-3.2.1v2-local-agent`

## Parent
The Phase 3.2.1v2 local-agent stem is based on the post-3.1.18 development
baseline and must remain separate from `main` until reviewed.

## Purpose
Re-verify and extend the controlled local development agent. The active Stem
runs the three standard real-AIOS regression queries and returns a single JSON
report with bounded per-query execution.

## Current status
- Local-agent foundation, launcher, controlled query action, and path handling
  are present on this branch.
- Autonomous R1/R2/R3 execution, JSON report-level tests, and a timeout smoke
  gate have passed.

## Test gates
- Focused local-agent unit tests: passed.
- One-second-per-query smoke regression: passed as a runner test; every case
  was reported as `timeout` without a hang.
- Existing Coordinator suite: 53 passed.
- Full 300-second-per-query live regression completed in 747.8 seconds:
  - R1 `current weather in philippines`: timed out at 300.1 seconds after
    search and answerability acceptance, during model generation.
  - R2 `tallest mountain in the philippines`: timed out at 300.3 seconds;
    routing incorrectly selected `Use Search: False` (`Travel handled locally`).
  - R3 `what is 2+2`: passed, returned `4`, in 147.3 seconds; model execution
    alone took 123.3 seconds.
- The runner correctly captured every terminal result; R1/R2 are AIOS failures,
  not local-agent runner failures.

## Boundaries
- Keep Coordinator as coordinator; local-agent owns process driving and result
  capture only.
- Do not merge this Stem into `main` directly.
- Start routing and generation-latency investigations on separate Stems.
