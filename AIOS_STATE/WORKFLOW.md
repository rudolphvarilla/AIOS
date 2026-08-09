# AIOS Repository Workflow

## Before implementation

Use the short repository commands explicitly:

- **pull** — synchronize the local working tree from the repository before implementation.
- **fetch** — inspect remote code/state when only inspection is needed.

Then read:
- `AIOS_STATE/INDEX.md`
- `AIOS_STATE/CURRENT_PHASE.md`
- `AIOS_STATE/CURRENT_BRANCH.md`
- the source/test files named by those files.

## During implementation

- Keep phase work separate from temporary experiments.
- Add regression tests with behavior changes.
- Prefer small named phase increments.
- Do not silently change retry semantics, public return contracts, or termination behavior.
- If work is paused, record the pause rather than relying on chat history.

## After implementation

Run focused tests first, then the full suite.

When green:

- **push** — publish the tested branch.
- **merge** — integrate a completed branch/PR into its intended parent.

`push` and `merge` are separate operations.

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
