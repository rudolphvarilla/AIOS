# Current Phase

## Active phase
**Phase 3.1.16 — Semantic Builder / Judge / Manager loop**

## Goal
Complete the first real semantic feedback-control loop around search/evidence construction:

1. Builder creates the evidence dataset from the original request.
2. Judge evaluates it using deterministic semantic/evidence validators.
3. Judge returns structured feedback when it fails.
4. Manager sends the original query plus that feedback back to Builder.
5. Builder produces an enriched retry instead of blindly repeating the same request.
6. Manager stops on acceptance or an explicit termination condition.
7. On retry-budget exhaustion, Manager returns the best validated attempt rather than losing useful work.

Do not advance to answer synthesis, durable memory, or autonomous scheduling until this loop is reliable.

## Completed before 3.1.16
- 5WH semantic understanding and alignment.
- Multi-provider search aggregation.
- Answerability validation.
- Deterministic ambiguous-sense resolution.
- Source-grounded deterministic fact extraction.
- Fact-aware answerability.
- Regression coverage for the above.

## Implementation contract

### Builder
- retain `original_query` unchanged;
- construct the current semantic/search request;
- accept judge feedback as retry context;
- incorporate feedback into the next build;
- expose enough attempt state for comparison.

### Judge
- evaluate the built evidence dataset;
- reuse deterministic validators;
- return structured pass/fail state;
- return actionable failure feedback;
- never upgrade source evidence into unsupported interpretations.

### Manager
- call Builder -> Judge repeatedly;
- interpret `max_retries` as retries **after** the initial attempt;
- pass judge feedback into the next Builder attempt;
- detect repeated identical builds;
- stop on acceptance;
- stop after the retry budget;
- return the best validated attempt when exhausted;
- preserve attempt history and stop reason.

## Current failing regression
Latest developer-reported full suite:

- 51 tests collected
- 50 passed
- 1 failed
- `tests/search/test_semantic_loop_manager.py::test_manager_returns_best_validated_attempt_when_retry_budget_exhausts`
- observed `pipeline.calls == 2`
- expected `pipeline.calls == 3`
- test passes `max_retries=2`, defining the contract as initial attempt + 2 retries = 3 calls.

## Immediate task
Fix Manager retry-budget semantics, then run the full suite.

## Acceptance criteria
- [ ] failing retry-budget test passes with exactly 3 calls;
- [ ] all semantic-loop tests remain green;
- [ ] full `python -m pytest -v` passes;
- [ ] attempt history remains available;
- [ ] builder feedback injection remains intact;
- [ ] repeated-query termination remains intact;
- [ ] 5WH, answerability, and source-grounded fact behavior is unchanged.

## Next phase
**Phase 3.1.17 — semantic loop quality and observability**

Candidate work: richer feedback categories, attempt scoring/comparison, explicit stop reasons, loop metrics, progressive-enrichment tests, and persistent project-state updates.

Do not start 3.1.17 until 3.1.16 is green.
