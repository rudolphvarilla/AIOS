# AIOS Project Roadmap

## North-star goal

Build AIOS as an autonomous personal AI operating system: one assistant/coordinator that can understand intent, plan work, use specialized capabilities, validate evidence/results, retain useful state, and execute long-running tasks safely and transparently.

The architecture should remain modular so models, search providers, tools, memory systems, and execution backends can be replaced without rewriting the coordinator.

## Roadmap

### Phase 1 — Core foundation
**Goal:** establish the executable coordinator and basic request lifecycle.

Core areas established in this phase include the coordinator, request/context state, model selection, routing, and basic execution plumbing.

Representative components visible in the repository history:
- `Coordinator/core/context/` — request/context analysis and result state.
- `Coordinator/core/keywords/` — deterministic keyword/domain registries and matching.
- `Coordinator/core/services/` — service/provider abstractions.
- Coordinator/model/router/planning components — choose capabilities and execution paths.

### Phase 2 — Coordinator intelligence and instrumentation
**Goal:** make routing/planning measurable and model-aware rather than a single hard-coded path.

Important responsibilities:
- model registry and model selection;
- coordinator state and execution planning;
- capability routing;
- performance instrumentation;
- deterministic fallbacks where appropriate.

### Phase 3 — Semantic search and evidence intelligence
**Goal:** turn raw search into a validated, source-grounded evidence dataset that an answering model can safely consume.

Phase 3 is intentionally layered. The system should not jump directly from query -> LLM answer.

#### 3.1 Semantic understanding and search validation

| Phase | Purpose | Key repository areas/classes |
|---|---|---|
| 3.1.12 | 5WH semantic search validation | `core/semantics/`, `core/search/fivewh_validator.py`, search context/evaluation |
| 3.1.13 | Multi-provider search aggregation | `core/search/aggregator.py`, provider manager selection, `SearchService` |
| 3.1.14 | Answerability evidence gate | `core/search/answerability.py`, `FactAwareAnswerabilityValidator`, `SearchEvaluator` |
| 3.1.15 | Deterministic sense resolution + fact extraction | `core/context/sense.py`, `SenseResolver`, `core/search/fact_extractor.py`, `SearchFact`, fact-aware answerability |
| 3.1.16 | Semantic Builder/Judge/Manager retry loop | semantic loop builder, judge, manager, retry/termination policy, regression tests |

> **Current repository visibility note:** the remote repository snapshot available while this state file was created exposes the 3.1.14 branch and its 3.1.14/3.1.15 changes through the open PR history. The latest local test output reported by the developer is Phase 3.1.16 with 51 tests and one retry-budget failure. That local state must be pushed before this roadmap can be considered a byte-for-byte inventory of the latest branch.

#### Builder / Judge / Manager architecture

Phase 3.1.16 is the first explicit control-loop layer:

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

**Builder**
- preserves the original user query;
- constructs/reconstructs the search/evidence dataset;
- incorporates judge feedback on retry;
- should enrich rather than blindly repeat the previous attempt.

**Judge**
- checks deterministic semantic alignment and answerability;
- returns structured failure reasons rather than a vague boolean;
- should explain what evidence/semantic slot is missing or inadequate.

**Manager**
- owns the retry loop;
- passes the original query and judge feedback back to the builder;
- records attempts;
- terminates on acceptance, retry-budget exhaustion, repeated identical builds, or another explicit stop condition;
- returns the best validated attempt when the retry budget is exhausted.

### Phase 4 — Answer synthesis and tool-aware execution
**Goal:** pass only validated evidence to the appropriate LLM/tool executor and preserve provenance into the final answer.

Expected areas:
- answer synthesis;
- citation/source rendering;
- tool invocation based on validated intent;
- explicit distinction between source facts and model inference;
- structured final response state.

### Phase 5 — Memory and long-running task state
**Goal:** give AIOS durable memory and background task continuity.

Expected areas:
- short/long-term memory;
- vector/graph retrieval;
- task state persistence;
- background scheduler;
- resumable workflows;
- result caching.

### Phase 6 — Autonomous operating system layer
**Goal:** coordinate multiple agents/services and execute multi-step tasks with supervision, permissions, and recovery.

Expected areas:
- agent/tool registry;
- permissions and safety boundaries;
- background jobs;
- event-driven triggers;
- task queues;
- failure recovery;
- observability.

### Stable release
**Goal:** a dependable personal AIOS that can run continuously and recover from ordinary failures without losing task state.

Acceptance characteristics:
- deterministic tests remain green;
- search/evidence loops terminate predictably;
- source provenance survives all transformations;
- model failures have fallbacks;
- long-running tasks are resumable;
- architecture is documented by code and state files.

### Expanded AIOS
**Goal:** optional integrations and advanced capabilities without destabilizing the core.

Examples:
- travel monitoring;
- academic assistant workflows;
- photography/event workflows;
- NAS/storage services;
- local model execution;
- application generation;
- external APIs and automation.

Expanded capabilities must plug into the coordinator instead of becoming special cases inside core semantic/search logic.

## Inventory rule

When adding/removing/refactoring a class or file, update the relevant phase entry and the current-phase state. The roadmap describes **responsibility**, not implementation detail. The code remains authoritative for exact behavior.
