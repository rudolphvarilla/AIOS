# AIOS State Index

Start here when resuming work.

1. Read `CURRENT_PHASE.md` — what we are solving now and what must be true before advancing.
2. Read `CURRENT_BRANCH.md` — what is being changed right now, including temporary work and branch status.
3. Read `PROJECT_ROADMAP.md` — why the current task exists and where it fits in the complete AIOS plan.
4. Read the actual source/test files named by those state files.

## Authority order

1. **Code + tests** — exact implementation behavior.
2. **PROJECT_ROADMAP.md** — intended architecture and phase boundaries.
3. **CURRENT_PHASE.md** — current goal and acceptance criteria.
4. **CURRENT_BRANCH.md** — temporary/active work state.
5. Chat history — context only, never the project's sole memory.

## Fast resume rule

A new session should be able to identify the current goal without reading the entire conversation. If these files disagree with the code, inspect the code/tests and then update the state files.
