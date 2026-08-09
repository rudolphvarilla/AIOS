# AIOS Repository Workflow

## Before implementation

State the intended repository action clearly and synchronize first:

- `pull` — update the local working tree from the repository.
- `fetch` — inspect remote code/state without changing local work.

Then read:
- `AIOS_STATE/INDEX.md`
- `AIOS_STATE/CURRENT_PHASE.md`
- `AIOS_STATE/CURRENT_BRANCH.md`

## During implementation

- Keep phase work separate from temporary experiments.
- Add regression tests with every behavior change.
- Prefer small, named phase increments.
- Do not silently change retry semantics, public return contracts, or termination behavior.
- If a task is blocked, update the state file instead of relying on conversation memory.

## After implementation

Run the focused tests first, then the full suite.

When green:

- `push` — publish the tested branch.
- `merge` — integrate the branch only when explicitly requested/appropriate.

`push` and `merge` are deliberately separate operations.

## Temporary experiment pattern

```text
active phase branch
       |
       +---- temporary experiment branch
       |          |
       |          +-- solve/test
       |          |
       |          +-- success -> incorporate deliberately
       |          |
       |          +-- failure -> document and discard
       |
       +---- continue phase
```

This prevents one-off debugging changes from silently becoming architecture.
