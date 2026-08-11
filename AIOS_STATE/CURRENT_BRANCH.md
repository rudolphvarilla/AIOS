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
- Run the normal 300-second regression separately to assess real AIOS behavior;
  its case outcomes are AIOS evidence, not local-agent runner failures.

## Boundaries
- Keep Coordinator as coordinator; local-agent owns process driving and result
  capture only.
- Do not merge this Stem into `main` directly.
- Record the normal regression outcome here before beginning another task.
