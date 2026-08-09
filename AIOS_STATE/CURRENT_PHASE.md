# Current Phase — Phase 3.1.18

## Goal
Stabilize the repository baseline while preserving the Phase 3 semantic architecture and make the full test suite runnable from a clean checkout.

## Current tasks
1. Restore prompt-builder/planner compatibility with the state objects used by tests.
2. Restore the CapabilityRouter call contract without weakening current routing behavior.
3. Align the DuckDuckGo service/test boundary with the SearchResult model.
4. Restore the expected SearchService module boundary.
5. Run the complete suite with no collection errors.
6. Preserve the Builder → Judge → Manager semantic feedback loop.

## Acceptance criteria
- `python -m pytest -v` collects the full suite without collection errors.
- All collected tests pass.
- No Phase 3 semantic-loop behavior is removed merely to satisfy legacy tests.
- Project-state files remain synchronized with the actual branch/task.

## Branch
`phase-3.1.18-stabilization`
