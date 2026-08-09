# AIOS Project State

This directory is the project's compact operational memory.

## Purpose

The repository is the source of truth for code. `AIOS_STATE/` is the source of truth for **project intent, roadmap, phase goals, and active work state** so a future session can resume without reconstructing the plan from chat history.

## Files

- `PROJECT_ROADMAP.md` — long-lived architecture roadmap from the initial build through stable and expanded AIOS. It records major phases and the important files/classes that implement each phase.
- `CURRENT_PHASE.md` — the active phase, its goal, current tasks, acceptance criteria, and known blockers. Update this when the phase advances or its goal changes.
- `CURRENT_BRANCH.md` — the current working branch/task. Use this for temporary work, experiments, fixes, and paused side work. When the work is accepted, fold the result into the appropriate phase and update this file.

## Builder / Judge / Manager

The semantic workflow is explicitly part of Phase 3:

1. **Builder** constructs the search/evidence dataset from the user's query and available evidence.
2. **Judge** evaluates whether the constructed dataset is sufficiently aligned and answer-bearing.
3. **Manager** decides whether to pass the validated dataset onward or send the builder back with structured failure feedback.
4. On retry, the builder receives the original query plus the judge's failure reason and produces an enriched attempt.
5. The loop stops when the judge accepts the attempt or the manager reaches its retry/termination policy.

The loop itself is not a replacement for deterministic validators. Validators are judges' instruments; the manager owns retry/termination behavior.

## Update rules

- Do not use chat history as the only project memory.
- Before changing architecture, read `PROJECT_ROADMAP.md` and `CURRENT_PHASE.md`.
- Before changing a temporary branch/task, read and update `CURRENT_BRANCH.md`.
- If a file/class becomes obsolete, update the roadmap when it is removed or replaced.
- If a phase is paused, leave the phase goal intact and record the pause in `CURRENT_BRANCH.md`.
- If an experiment succeeds, document how it is incorporated into the phase. If it fails, record why so the same path is not repeated blindly.
- Keep these files concise enough to scan quickly; detailed implementation belongs in code and tests.

## Workflow vocabulary

- **pull** — synchronize the local working copy from the repository before implementation.
- **fetch** — retrieve repository state/code for inspection without changing the working copy.
- **push** — publish completed, tested changes.
- **merge** — integrate a completed branch/PR into its intended parent. Do not infer that `push` means `merge`.
