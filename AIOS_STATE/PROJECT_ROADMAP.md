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

### Phase 3 — Context Intelligence
**Goal:** turn raw search into a validated, source-grounded evidence dataset and iteratively improve that context before downstream reasoning.

Phase 3 is intentionally layered:

```text
query
  -> semantic understanding
  -> evidence construction
  -> validation
  -> iterative context construction
  -> validated context
  -> downstream reasoning
```

The phase is divided into three architectural milestones. The historical 3.1.x implementation sequence remains valid Git history, but the responsibility boundary is now documented explicitly as 3.1 / 3.2 / 3.3.

#### 3.1 — Semantic Context & Deterministic Evidence
**Status: COMPLETE**

Responsibilities:
- semantic understanding
- keyword enrichment
- sense resolution
- context aggregation
- search evidence
- deterministic fact extraction
- source-grounded statements
- answerability
- evidence validation

The completed 3.1.x implementation sequence included:

| Historical phase | Purpose |
|---|---|
| 3.1.12 | 5WH semantic search validation |
| 3.1.13 | Multi-provider search aggregation |
| 3.1.14 | Answerability evidence gate |
| 3.1.15 | Deterministic sense resolution + fact extraction |
| 3.1.16 | Semantic Builder/Judge/Manager retry loop foundation |
| 3.1.17 | Project-state continuity baseline |
| 3.1.18 | Stabilization and integration verification |

The historical 3.1.16 Builder/Judge/Manager work is also the foundation for the architectural 3.2 milestone below. It is not duplicated or discarded; 3.2 completes and hardens that iterative-context responsibility.

#### 3.2 — Iterative Context Construction
**Status: CURRENT**

**Goal:** iteratively construct a stronger evidence context by evaluating the current context, identifying deficiencies, enriching/rebuilding the context, and terminating deterministically when the context is accepted or cannot be improved further.

Core responsibilities:
- **Builder** — construct or reconstruct the evidence/search dataset, preserve the original query, and incorporate structured Judge feedback.
- **Judge** — evaluate semantic alignment, evidence quality, and answerability; return structured reasons for failure or acceptance.
- **Manager** — own attempt history, retry counting, feedback propagation, repeated-build detection, acceptance, and retry-budget termination.
- **Feedback loop** — carry structured deficiencies from Judge to Builder for subsequent attempts.
- **Enrichment** — deliberately address identified evidence/context gaps rather than performing blind retries; preserve useful evidence across attempts where appropriate and avoid duplicate evidence.
- **Termination policy** — distinguish accepted context, retryable deficiency, stagnation/repeated build, retry-budget exhaustion, and inability to enrich further.
- **Validated context contract** — produce a stable downstream object containing the original query, semantic requirements, evidence/provenance, evaluation state, enrichment/attempt history, answerability, and termination state.

Target loop:

```text
Original Query
     |
     v
  BUILDER  ---> evidence/search dataset
     |
     v
   JUDGE   ---> pass / fail + structured deficiency
     |
     +---- PASS ----> validated context
     |
     +---- FAIL ----> MANAGER records attempt
                         |
                         v
                  enrichment strategy
                         |
                         v
                    BUILDER + feedback
                         |
                         +----> next attempt
```

Existing Builder/Judge/Manager implementation and regression tests are the foundation. Phase 3.2 work should finish the enrichment, evidence-preservation/fusion, deficiency representation, and explicit termination contracts rather than replacing the existing loop.

#### 3.3 — AIOS Integration, Validation & Output Architecture
**Status: PLANNED**

**Goal:** prove the completed Phase 3 system through the actual AIOS execution path, then cleanly separate development diagnostics from user-facing output and bring command documentation up to date.

Responsibilities:
- full end-to-end AIOS regression testing through the real Coordinator pipeline;
- realistic search, ambiguous-query, insufficient-evidence, retry, enrichment, and final-response scenarios;
- integration validation of Builder/Judge/Manager inside actual AIOS execution;
- development-output refactor so diagnostic/debug output is separated from production/user-facing output;
- keep `coordinator.py` focused on coordination rather than accumulating output/debug responsibilities;
- centralize or structure development diagnostics so they remain available during development without contaminating normal output;
- refactor `/help` so it reflects the current command/test/development capabilities and does not become stale;
- verify the final Phase 3 contract and regression behavior before advancing to Phase 4.

Phase 3.3 is the integration gate for Phase 3. Unit and focused integration tests remain necessary, but completion also requires the actual AIOS pipeline to exercise the completed system.

### Phase 4 — Answer Synthesis and Tool-Aware Execution
**Goal:** pass only validated context to the appropriate answering model/tool executor and preserve provenance into the final response.

This is the first major downstream reasoning/execution layer built on top of Phase 3's validated context. It is the foundation for the broader autonomous-reasoning direction of AIOS.

Expected areas:
- answer synthesis
- citation/source rendering
- tool invocation
- source-fact versus model-inference distinction
- final response state
- controlled multi-step tool execution
- execution-result validation and recovery

Phase 4 must consume the Phase 3 validated-context contract rather than bypassing evidence validation with a direct search-to-LLM path.

### Phase 5 — Memory and Long-Running Task State
**Goal:** durable memory, background task continuity, caching, resumable workflows, and scheduler state.

Expected areas include persistent useful state, task continuation, cached results, background scheduling, and safe resumption of interrupted work.

### Phase 6 — Autonomous Operating System Layer
**Goal:** multi-agent/tool coordination, permissions, event triggers, task queues, recovery, and observability.

Expected areas include specialized agents, event-driven execution, permissions, task orchestration, recovery, and long-running autonomous operation.

### Stable AIOS
A dependable continuously running personal AIOS with predictable termination, provenance preservation, fallbacks, resumable tasks, and green regression tests.

### Expanded AIOS
Optional integrations such as travel monitoring, academic workflows, photography/event systems, NAS/storage, local models, application generation, and external automation. These must plug into the coordinator rather than become special cases in core semantic/search logic.

## Development and local-agent workflow

AIOS development is expected to support a local coding agent capable of inspecting the repository, running tests, making controlled changes, and reporting command results. The development agent is tooling around AIOS, not part of the runtime coordinator architecture.

The preferred separation is:

```text
Project architecture / design / review
        |
        v
   ChatGPT / project control
        |
        v
Local coding agent (Codex)
        |
        +-- inspect repository
        +-- edit implementation
        +-- run pytest/regression tests
        +-- inspect failures
        +-- perform controlled Git operations
        +-- report results
```

Merge-to-main and destructive repository operations should remain explicitly controlled until the local-agent workflow has been validated.

## Inventory rule

When a file/class is added, removed, renamed, refactored, or made obsolete, update the phase inventory and current state. The roadmap describes responsibility; the code and tests remain authoritative for exact behavior.

## Current synchronization state

Phase 3.1.18 stabilization has been merged into `main`. The full test suite at the Phase 3.1.18 stabilization checkpoint is green at **53/53 tests passed**.

A full repository-state backup was created before Phase 3.2 documentation work:

- `backup/phase-3.1.18-main-2026-08-11`

Phase 3.2.0 is the documentation reconciliation and backup checkpoint. Phase 3.2.1 will establish and test the local development agent workflow before implementation of the remaining Phase 3.2 functionality.

Do not advance to Phase 4 until Phase 3.2 and Phase 3.3 are explicitly completed and the full Phase 3 acceptance gate is green.
