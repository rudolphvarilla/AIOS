# AIOS Project State

`AIOS_STATE/` is the project's compact operational memory.

The repository is the source of truth for code. These files are the source of truth for project intent, roadmap, phase goals, and active work state so a future session can resume without reconstructing the plan from conversation history.

## Files

- `INDEX.md` — fast resume entry point and authority order.
- `PROJECT_ROADMAP.md` — long-lived architecture roadmap from foundation through stable and expanded AIOS.
- `CURRENT_PHASE.md` — active phase, goal, acceptance criteria, and blockers.
- `CURRENT_BRANCH.md` — current branch/task and temporary-work state.
- `WORKFLOW.md` — pull/fetch/push/merge workflow and experiment isolation.
- `BRANCH_TEMPLATE.md` — template for temporary branch records.

## Builder / Judge / Manager

Phase 3 semantic search uses the requested control-loop model:

1. Builder constructs the evidence dataset.
2. Judge determines whether it passes semantic/evidence gates.
3. Manager passes validated data onward or loops back to Builder with structured failure feedback.
4. Builder enriches the next attempt using the original query plus the judge's feedback.
5. The loop terminates on acceptance or an explicit retry/termination policy.

Deterministic validators are the Judge's instruments; the Manager owns retry and termination behavior.

## Update rules

- Before architecture changes, read the roadmap and current phase.
- Before temporary work, update the branch state.
- When files/classes are added, removed, renamed, or made obsolete, update the roadmap inventory.
- When a phase is paused, keep its goal intact and record the pause in branch state.
- When an experiment succeeds, record how it is incorporated. When it fails, record why.
- Keep state files concise; implementation details belong in code/tests.

## Authority order

1. Code + tests
2. `PROJECT_ROADMAP.md`
3. `CURRENT_PHASE.md`
4. `CURRENT_BRANCH.md`
5. Chat history

Chat is context, not the project's only memory.
