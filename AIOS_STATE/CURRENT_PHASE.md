# Current Phase

## Active phase
**Phase 3.1.16 — Semantic Builder / Judge / Manager loop**

## Phase goal
Complete the first real semantic feedback-control loop around search/evidence construction:

1. Builder creates the evidence dataset from the original request.
2. Judge evaluates the dataset using deterministic semantic/evidence validators.
3. Judge returns structured feedback when the dataset fails.
4. Manager sends the original query plus that feedback back to Builder.
5. Builder creates an enriched retry rather than blindly repeating the same request.
6. Manager stops on judge acceptance or an explicit termination condition.
7. If the retry budget is exhausted, Manager returns the best validated attempt rather than losing all useful work.

This is the current focus. Do **not** jump to answer synthesis, memory, or autonomous scheduling until this loop is reliable.

## Completed immediately before this phase
- 5WH semantic understanding and alignment.
- Multi-provider search aggregation.
- Answerability validation.
- Deterministic ambiguous-sense resolution.
- Source-grounded deterministic fact extraction.
- Fact-aware answerability.
- Regression coverage for the above.

## Current implementation contract

### Builder
The builder must:
- retain `original_query` unchanged;
- construct the current `semantic_query`/search request;
- accept judge feedback as retry context;
- incorporate feedback into the next build;
- expose enough attempt state for the manager to compare attempts.

### Judge
The judge must:
- evaluate the built evidence dataset;
- reuse existing deterministic validators rather than duplicating their logic;
- return a structured pass/fail decision;
- return actionable feedback naming what failed;
- avoid turning source evidence into unsupported interpretations.

### Manager
The manager must:
- call Builder -> Judge repeatedly;
- count attempts consistently;
- provide judge feedback to the next Builder attempt;
- detect repeated identical builds;
- stop on acceptance;
- stop on retry budget exhaustion;
- return the best validated attempt available when exhausted;
- preserve the attempt history for diagnostics.

## Current failing regression
Latest developer-reported full suite:

- **51 collected**
- **50 passed**
- **1 failed**
- failing test: `tests/search/test_semantic_loop_manager.py::test_manager_returns_best_validated_attempt_when_retry_budget_exhausts`
- observed: `pipeline.calls == 2`
- expected: `pipeline.calls == 3`
- test uses `max_retries=2` and therefore defines the intended contract as **initial attempt + 2 retries = 3 pipeline calls**.

### Immediate task
Fix Manager retry-budget semantics so `max_retries` means the number of retries *after the initial build*, then run the full test suite.

### Acceptance criteria
- The failing regression passes with exactly 3 pipeline calls.
- Existing semantic-loop tests remain green.
- Full `pytest -v` passes.
- Attempt history remains available.
- Builder feedback injection remains intact.
- Repeated-query termination still works.
- No change weakens 5WH, answerability, or source-grounded fact behavior.

## Next phase after this is green
**Phase 3.1.17 — strengthen semantic loop quality and observability.**

Likely work:
- richer structured feedback categories;
- attempt scoring/comparison;
- explicit stop reasons;
- loop metrics;
- tests for progressive enrichment rather than merely retry count;
- persistent project-state updates.

Do not start 3.1.17 until 3.1.16 acceptance criteria are green.
