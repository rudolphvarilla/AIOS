# Current Branch / Task

## Branch
`phase-3.1.17-project-state`

## Parent phase
Phase 3.1.16 semantic Builder/Judge/Manager loop

## Purpose
Create durable project memory inside the repository so future sessions can resume from code + state files instead of reconstructing the project from chat history.

## Current task
Add the project-state file series and preserve the current Phase 3.1.16 retry-budget failure as the active implementation task.

## Important synchronization fact
The remote repository currently exposes Phase 3.1.14 as its newest development branch, while the developer's local workspace is reported to be at Phase 3.1.16. This branch therefore documents the reported local state but does not claim to contain the local 3.1.16 implementation.

## Tests reported before this branch
`python -m pytest -v`

- 51 collected
- 50 passed
- 1 failed
- retry-budget exhaustion test expects 3 calls for `max_retries=2`, but observed 2.

## Work boundaries
Do:
- keep the state files concise and authoritative about intent;
- fix the retry-count contract in the actual 3.1.16 branch after it is synchronized to GitHub;
- preserve builder feedback, repeated-build termination, and best-attempt fallback.

Do not:
- bypass the Judge to make tests pass;
- weaken deterministic validators;
- start Phase 4 before Phase 3.1.16 is green;
- mix unrelated experiments into the active phase.

## Temporary branch rule
For a one-off experiment, create a separate branch and record its purpose here. If successful, incorporate it deliberately. If unsuccessful, record the reason and discard it.

## Completion
After the state-system branch is accepted:
1. synchronize/pull the latest implementation branch;
2. fix the 3.1.16 retry-budget failure;
3. run focused tests;
4. run full suite;
5. update `CURRENT_PHASE.md`;
6. push;
7. merge only when explicitly requested.
