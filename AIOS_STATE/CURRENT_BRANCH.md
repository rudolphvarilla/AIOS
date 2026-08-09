# Current Branch / Task

## Branch state
**Remote branch containing this state file:** `phase-3.1.14-answerability`

**Intended local working state:** the developer reports the local workspace has progressed through **Phase 3.1.16** and currently has 51 tests with one retry-budget failure.

> The GitHub remote visible to the coordinator currently exposes Phase 3.1.14 as the newest open branch/PR. Therefore this file deliberately distinguishes the remote branch from the reported local branch state instead of pretending the remote already contains 3.1.16.

## Active task
Fix:
`tests/search/test_semantic_loop_manager.py::test_manager_returns_best_validated_attempt_when_retry_budget_exhausts`

Expected contract:
- `max_retries=2`
- initial build = attempt 1
- retry 1 = attempt 2
- retry 2 = attempt 3
- therefore `pipeline.calls == 3`

## Why this task exists
The Builder/Judge/Manager loop is now present conceptually and under test. The remaining failure is a manager accounting/termination detail: the retry budget is currently being interpreted as the total number of pipeline calls rather than retries after the initial attempt.

## Work boundaries
Do:
- inspect the semantic loop manager and its tests;
- correct retry counting;
- preserve structured judge feedback;
- preserve repeated-query termination;
- preserve best-attempt fallback;
- add/adjust regression coverage if needed.

Do not:
- rewrite the deterministic search validators;
- remove answerability checks;
- bypass the judge to make tests pass;
- change `max_retries` semantics elsewhere without a regression test.

## Completion procedure
1. Run the focused semantic-loop manager tests.
2. Run `python -m pytest -v`.
3. If green, update `CURRENT_PHASE.md` to mark 3.1.16 complete and identify the next phase.
4. Update this file to describe the next active branch/task.
5. Commit and push.
6. Only merge when explicitly requested or when the branch/PR workflow calls for merge.

## Temporary-work rule
If an unrelated experiment is needed, create a separate branch first and record it here. If successful, incorporate it deliberately into the active phase. If abandoned, leave a short reason and return to this task without contaminating the phase branch.
