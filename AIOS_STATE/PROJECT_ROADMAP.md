# AIOS Project Roadmap

## North-star goal

Build AIOS as an autonomous personal AI operating system: one assistant/coordinator that can understand intent, plan work, use specialized capabilities, validate evidence/results, retain useful state, and execute long-running tasks safely and transparently.

The architecture remains modular so models, search providers, tools, memory systems, and execution backends can be replaced without rewriting the coordinator.

## Roadmap

### Phase 1 — Core foundation
**Goal:** establish the executable coordinator and basic request lifecycle.

Representative areas visible in repository history:
- `Coordinator/core/context/` — request/context analysis and result state.
- `Coordinator/core/keywords/` — deterministic keyword/domain registries and matching.
- `Coordinator/core/services/` — service/provider abstractions.
- coordinator/model/router/planning components — choose capabilities and execution paths.

### Phase 2 — Coordinator intelligence and instrumentation
**Goal:** make routing, planning, model selection, and execution measurable rather than one hard-coded path.

Responsibilities include model registry/selection, coordinator state, capability routing, performance instrumentation, and deterministic fallbacks.

### Phase 3 — Semantic search and evidence intelligence
**Goal:** turn raw search into a validated, source-grounded evidence dataset that an answering model can safely consume.

Phase 3 is intentionally layered: query -> validated evidence -> downstream reasoning, not query -> unchecked LLM answer.

#### 3.1 Semantic understanding and search validation — COMPLETE

| Phase | Purpose | Key files/classes |
|---|---|---|
| 3.1.12 | 5WH semantic search validation | `core/semantics/`, `core/search/fivewh_validator.py`, search context/evaluation |
| 3.1.13 | Multi-provider search aggregation | `core/search/aggregator.py`, provider manager selection, `SearchService` |
| 3.1.14 | Answerability evidence gate | `core/search/answerability.py`, `FactAwareAnswerabilityValidator`, `SearchEvaluator` |
| 3.1.15 | Deterministic sense resolution + fact extraction | `core/context/sense.py`, `SenseResolver`, `core/search/fact_extractor.py`, `SearchFact` |
| 3.1.16 | Semantic Builder/Judge/Manager retry loop | semantic loop builder/judge/manager, retry/termination policy, regression tests |
| 3.1.17 | Project-state continuity baseline | `AIOS_STATE/`, repository-resume workflow, persistent phase/branch/task records |
| 3.1.18 | Stabilization and integration verification | retry/contract repairs, answerability precedence, semantic-loop integration tests, full-suite verification |

#### Builder / Judge / Manager

```text
Original Query
     |
     v
  BUILDER  ---> evidence/search dataset
     |
     v
   JUDGE   ---> pass / fail + structured feedback
     |
     +---- PASS ----> validated dataset -> downstream LLM
     |
     +---- FAIL ----> MANAGER records attempt
                         |
                         v
                    BUILDER + feedback
                         |
                         +----> next attempt
```

**Builder** constructs or reconstructs the dataset, preserves the original query, and injects judge feedback into retries.

**Judge** evaluates semantic alignment and answerability, returning structured reasons for failure.

**Manager** owns retry counting, feedback propagation, attempt history, repeated-build detection, acceptance, and retry-budget termination.

#### 3.2 Iterative Context Construction — CURRENT

**Purpose:** complete the connection between the Phase 3.1 semantic/evidence system and actual AIOS execution. Phase 3.2 is not a replacement for Builder/Judge/Manager; it closes the integration and contract gaps required for validated Phase 3 context to become usable by the real AIOS pipeline.

The work proceeds from the post-3.1.18 `main` baseline and must be verified through the actual AIOS execution path.

Planned progression:

- **3.2.0 — Documentation reconciliation and project backup**
  - establish the post-3.1.18 baseline;
  - preserve a full backup of the pre-3.2 state;
  - synchronize project state documentation.
- **3.2.1 — Local agent setup and testing**
  - establish a local development-agent workflow;
  - verify repository/terminal access and regression-test execution;
  - determine whether local Git/test operations can be delegated safely.
- **3.2.2 — Phase 3.1 → AIOS integration-gap audit**
  - trace the real Coordinator → Semantic Understanding → Planner → Router → Search → Phase 3.1 → Prompt Builder → LLM path;
  - identify where validated Phase 3 context is lost, flattened, bypassed, or improperly transformed;
  - determine the minimum changes required to make Phase 3.1 a real AIOS execution component.
- **3.2.x — Integration fixes and verification**
  - implement only confirmed gaps;
  - use Stems for significant experimental implementations;
  - test each accepted Stem against the real AIOS pipeline;
  - integrate successful Stems into the Current Goal and prune failed Stems.

### Stem workflow

A **Stem** is a temporary experimental branch used when an important function or implementation approach needs to be inserted and tested without committing the approach to the Current Goal.

```text
Current Goal
     |
     +---- Stem ---- test ---- FAIL ----> PRUNE
     |
     +---- Stem ---- test ---- PASS ----> INTEGRATE
                                          |
                                          v
                                    regression test
                                          |
                                          v
                                    update Current Goal
```

A Stem is not a permanent roadmap phase. It exists only to test a meaningful implementation hypothesis. A failed Stem is pruned; a successful Stem is integrated and then becomes part of the Current Goal after regression verification.

### Phase 3.3 — AIOS Integration Validation and Output Architecture
**Goal:** validate the completed Phase 3 system through the actual AIOS runtime and clean up the development-facing output architecture.

Planned areas:
- full AIOS end-to-end regression of Phase 3 implementations;
- development-output refactor so diagnostic/development output is separated from `coordinator.py` responsibilities;
- `/help` command refactor to reflect the current command/test surface;
- final Phase 3 acceptance gate.

### Phase 4 — Answer synthesis and tool-aware execution
**Goal:** pass only validated evidence to the appropriate LLM/tool executor and preserve provenance into the final answer.

Expected areas: answer synthesis, citation/source rendering, tool invocation, distinction between source facts and model inference, and final response state.

### Phase 5 — Memory and long-running task state
**Goal:** durable memory, background task continuity, caching, resumable workflows, and scheduler state.

### Phase 6 — Autonomous operating system layer
**Goal:** multi-agent/tool coordination, permissions, event triggers, task queues, recovery, and observability.

### Stable AIOS
A dependable continuously running personal AIOS with predictable termination, provenance preservation, fallbacks, resumable tasks, and green regression tests.

### Expanded AIOS
Optional integrations such as travel monitoring, academic workflows, photography/event systems, NAS/storage, local models, application generation, and external automation. These must plug into the coordinator rather than become special cases in core semantic/search logic.

## Inventory rule

When a file/class is added, removed, renamed, refactored, or made obsolete, update the phase inventory and current state. The repository file-tree/inventory document, once located or established, must remain synchronized with this roadmap. The roadmap describes responsibility; the code and tests remain authoritative for exact behavior.

## Current synchronization state

- `main` is the active development baseline after Phase 3.1.18 stabilization PR #10 was merged.
- `backup/phase-3.1.18-main-2026-08-11` preserves the pre-3.2 `main` state.
- The known Phase 3 regression baseline is **53/53 tests passed**.
- `phase-3.2.0v2-documentation-reconciliation` is the documentation-only reconciliation Stem/branch created from `main`.
- This documentation checkpoint must be integrated into `main` before 3.2.1/3.2.2 implementation work is advanced.

## Current Goal

**Phase 3.2 — Connect and harden Phase 3.1 into actual AIOS execution.**

Immediate task: **3.2.2v2 — audit the real Phase 3.1 → AIOS execution path and identify only the confirmed integration gaps.**

Do not redesign working Phase 3.1 components merely for architectural preference. Do not create new abstractions until the audit demonstrates that they are required by an actual integration gap.

After every successful test gate, update the Current Goal/state documentation before beginning the next task.

## State vocabulary

- **Project:** the long-term AIOS architecture and roadmap.
- **Current Goal:** the active implementation objective and immediate next task.
- **Stem:** a temporary experimental implementation branch for a meaningful hypothesis.
- **Prune:** abandon a failed Stem without integrating it.
- **Integrate:** merge a successful Stem into the Current Goal after verification.
