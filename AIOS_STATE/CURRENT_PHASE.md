# Current Phase

## Active phase
**Phase 3.2.1v2 — Local development-agent re-verification**

## Current goal
Provide a controlled local agent that can run the standard real-AIOS regression
queries through the existing Coordinator workflow and return one structured,
bounded report for inspection.

## Acceptance criteria
- `local_agent\run_agent.bat regression` runs R1 weather, R2 mountain, and R3
  arithmetic through `Coordinator/coordinator.py`.
- Every case records success, timeout/return status, stdout, stderr, and elapsed
  time in JSON.
- A timed-out Coordinator query returns a report rather than hanging the agent.
- Coordinator retains ownership of development output and execution.
- Local-agent tests pass before this Stem is integrated.

## Verified gate
- Focused local-agent unit tests passed.
- A one-second-per-query smoke regression reported all cases as `timeout` and
  exited normally, proving bounded timeout reporting.
- Existing Coordinator suite passed: 53 tests.

## Boundaries
- Do not modify `coordinator.py` for local-agent reporting.
- Do not expose a raw shell or remote transport.
- This work is a Phase 3.2.1v2 Stem; it does not alter the Phase 3.1 semantic
  search architecture.
