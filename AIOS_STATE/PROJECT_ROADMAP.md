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

#### 3.1 Semantic understanding and search validation

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

When a file/class is added, removed, renamed, refactored, or made obsolete, update the phase inventory and current state. The roadmap describes responsibility; the code and tests remain authoritative for exact behavior.

## Current synchronization state

Phase 3.1.18 stabilization has been pushed and rebased onto the current `main` baseline. The full test suite on the stabilization branch is green at **53/53 tests passed**. PR #10 is the delivery path from `phase-3.1.18-stabilization` into `main`.

Do not advance to a new phase until PR #10 is merged and the next phase is explicitly established from the repository state.
