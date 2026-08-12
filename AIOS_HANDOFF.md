# AIOS Handoff for Coding Assistants

This document is the durable starting point for an AI coding assistant taking
over AIOS work. Read it with `AIOS_STATE/INDEX.md`, then verify the working tree
before changing code. It is intentionally a summary and navigation map; the
code and tests are the authority for exact behavior.

## What AIOS is

AIOS is an **Artificial Intelligence Operating System**: a modular local
assistant that understands a request, selects capabilities and models, gathers
and validates evidence when needed, builds a controlled prompt, executes it,
and retains useful state. It is not meant to be a single raw LLM call.

The intended system flow is:

```text
User request
  -> semantic understanding / 5WH
  -> planning, decision, routing, model and tool selection
  -> optional live search
  -> validated evidence (Builder -> Judge -> Manager)
  -> prompt construction and model execution
  -> output, memory, background work, performance diagnostics
```

`Coordinator/coordinator.py` remains the interactive composition root and
Coordinator. Supporting runners must not move development-output ownership into
it.

## Resume protocol

1. Inspect `git status --short --branch` and do not erase unrelated changes.
2. Read, in order:
   - `AIOS_STATE/INDEX.md`
   - `AIOS_STATE/CURRENT_PHASE.md`
   - `AIOS_STATE/CURRENT_BRANCH.md`
   - `AIOS_STATE/PROJECT_ROADMAP.md`
   - this file.
3. Read the source and tests named by the active task before proposing a fix.
4. Use a focused **Stem** for a concrete hypothesis. Test it against both unit
   coverage and the real execution path. Prune it if it does not solve the
   demonstrated problem.
5. After a successful test gate, update the current goal and branch/stem files
   before beginning the next task. Commit deliberately; push and merge are
   separate actions. Never merge a stem directly into `main` without review.

The state-file authority order is: code/tests, roadmap, current phase, current
branch, then chat history.

## Current status and immediate task

Current branch: `phase-3.2.1v2-local-agent`.

The local-agent regression runner was implemented, tested, committed, and
pushed at `48e0fc3` (`feat: run standard AIOS queries from local agent`). It
runs the three real Coordinator queries and outputs one structured JSON report.
The runner itself is working; do not redesign it for the following AIOS failures.

Latest live regression, 2026-08-12, with a 300-second limit per case:

| Case | Query | Result | Evidence |
|---|---|---|---|
| R1 | `current weather in philippines` | timeout, 300.1s | `Use Search: True`; the complete search/evidence path ran and answerability was accepted at `1.00`; downstream model generation then stalled. |
| R2 | `tallest mountain in the philippines` | timeout, 300.3s | Incorrect route: `Use Search: False`, reason `Travel handled locally`; model generation then stalled. |
| R3 | `what is 2+2` | pass, 147.3s | Returned `4`; `Use Search: False` was correct; model execution took 123.3s. |

Current next steps, in separate stems:

1. Identify and correct the search-routing rule causing R2's factual geography
   query to be treated as local travel. Add a focused regression test first.
2. Diagnose the shared downstream model generation latency/timeout revealed by
   R1, R2, and R3. Preserve evidence handling while locating the bottleneck.
3. Re-run the standard live regression after each successful, targeted change.

Do not infer that search is broken from R1: its search pipeline succeeded. Do
not hide the latency by simply increasing the timeout without identifying why
generation is slow.

## Repository tree and navigation

```text
C:\AIOS\
├── AIOS_HANDOFF.md              # this durable assistant handoff
├── AIOS_STATE\                  # current goal, branch, roadmap, workflow
├── Coordinator\                 # runnable AIOS application
│   ├── coordinator.py            # interactive composition root / main loop
│   ├── core\                    # domain modules; see map below
│   ├── data\                    # local application data
│   ├── docs\                    # Coordinator documentation
│   ├── models\                  # model configuration/assets
│   └── tests\                   # 53-test Coordinator regression suite
├── local_agent\                 # controlled local development runner
│   ├── agent.py                 # allowlisted actions and JSON reports
│   ├── run_agent.bat            # Windows entry point
│   └── tests\test_agent.py      # local-agent unit tests
└── Qdrant\                      # local vector-store-related data/service
```

Generated directories such as `.venv`, `__pycache__`, and `.pytest_cache` are
not source architecture. Do not treat `*_backup.py` files as active code unless
the current import path shows otherwise.

## Code map: where functions and classes live

Start with `Coordinator/coordinator.py:main()`. It drives the pipeline and is
the best way to trace actual behavior. The active modules are organized by
responsibility:

| Area | Primary files/classes | Responsibility |
|---|---|---|
| Pipeline state/control | `core/execution/pipelinestate.py:PipelineState`, `pipeline_controller.py:PipelineController`, `semantic_phase.py:run`, `intent_phase.py:run`, `context_phase.py:run` | ordered request lifecycle and shared state |
| Semantic interpretation | `core/semantics/analysis.py:SemanticAnalysisEngine`, `fivewh.py:FiveWHUnderstanding`, `result.py:SemanticResult` | semantic domains and 5WH extraction |
| Intent, planning, routing | `core/intent/llm_understanding.py:SemanticUnderstanding`, `core/decision/engine.py:DecisionEngine`, `core/planner/planner.py:build_plan`, `core/routing/router.py:CapabilityRouter`, `core/router.py:route` | interpret and select capabilities/search/model path |
| Search service | `core/services/search_service.py:SearchService`, `core/providers/manager.py:ProviderManager`, `duckduckgo.py:DuckDuckGoProvider` | obtain live search results |
| Search processing | `core/search/pipeline.py:SearchPipeline`, `filter.py:SearchFilter`, `ranker.py:SearchRanker`, `deduplicator.py:SearchDeduplicator`, `extractor.py:SearchExtractor`, `fact_extractor.py:SearchFactExtractor` | turn raw results into structured evidence |
| Search validation loop | `core/search/semantic_loop.py:SemanticSearchBuilder`, `SemanticSearchJudge`, `SemanticSearchManager`; `evaluator.py:SearchEvaluator`; `answerability.py:AnswerabilityValidator`; `fact_aware_answerability.py:FactAwareAnswerabilityValidator` | Builder -> Judge -> Manager evidence gate and retry policy |
| Prompt/execution | `core/prompt/builder.py:PromptBuilder`, `core/prompt/planner.py:PromptPlanner`, `core/executor.py:execute`, `core/tools/manager.py:ToolManager` | assemble validated context and invoke execution |
| Memory | `core/memory/manager.py:MemoryManager`, `working_memory.py:WorkingMemory`, `session_memory.py:SessionMemory`, `core/longterm/manager.py:LongTermMemoryManager` | working, session, and long-term memory |
| Output/debugging | `core/output/presenter.py:Presenter`, `developer_output.py:DeveloperOutput`, `core/developer/manager.py:DeveloperMode`, `core/performance.py:PerformanceMonitor` | user output, developer diagnostics, timing |
| Background work | `core/scheduler/manager.py:Scheduler`, `queue.py:BackgroundQueue`, `worker.py:BackgroundWorker` | queued/resumable background jobs |
| Tests | `Coordinator/tests/` grouped by `search`, `semantics`, `services`, `longterm`, etc. | executable behavior contracts |

Use ripgrep to locate a symbol before editing, for example:

```powershell
rg -n "class CapabilityRouter|def route" C:\AIOS\Coordinator
rg -n "Use Search|Travel handled locally" C:\AIOS\Coordinator
rg -n "class SemanticSearch|Answerability" C:\AIOS\Coordinator\core\search
```

## Local-agent contract

Invoke it from the repository root or any Windows directory:

```bat
C:\AIOS\local_agent\run_agent.bat verify
C:\AIOS\local_agent\run_agent.bat git-status
C:\AIOS\local_agent\run_agent.bat query "what is 2+2"
C:\AIOS\local_agent\run_agent.bat regression
```

`regression` runs R1/R2/R3 in order. It retains per-case command, working
directory, return code, stdout, stderr, elapsed seconds, and status
(`passed`, `failed`, or `timeout`) in a JSON report. `--timeout N` controls the
per-query bound. A report with `ok: false` is expected when an AIOS case fails;
it does not by itself mean the runner is defective.

## Coding style and design preferences

The owner prefers code that explains its purpose before its mechanics:

- Put a descriptive documentation block immediately before a non-trivial class,
  function, or logical implementation block. State intent, inputs/outputs,
  invariants, and why the block exists—not a restatement of syntax.
- Use descriptive names. Favor explicit data flow and small modules over clever,
  compressed abstractions.
- Preserve modular boundaries: routing routes; search validates evidence;
  prompts compose context; Coordinator orchestrates. Avoid one-off special cases
  in `coordinator.py`.
- Keep deterministic validators authoritative. Do not weaken retry semantics or
  public result contracts without regression tests.
- Add or update focused tests whenever behavior changes. Test the real pipeline
  when a problem is integration-specific.
- Keep debug/development output separate from orchestration responsibility.
- Use UTF-8 for documentation so punctuation renders correctly.

## Documentation rules

`AIOS_STATE/` is operational memory, not a duplicate code manual:

- `CURRENT_PHASE.md`: the active goal, acceptance criteria, results, and next
  authorized task.
- `CURRENT_BRANCH.md`: the actual checked-out stem/branch, scope, test gates,
  and branch-specific findings.
- `PROJECT_ROADMAP.md`: long-lived architectural direction and phase inventory.
- `WORKFLOW.md`: branch/test/push/merge discipline.
- `AIOS_HANDOFF.md`: cross-assistant resume guide; update it when architecture,
  project location, coding conventions, v1.0 definition, or immediate task
  changes materially.

After every successful test gate, update current-phase and current-branch state
before starting the next task. Keep entries factual: command/test, outcome,
commit/branch, and remaining evidence-backed issue. Do not claim a capability
is complete merely because a unit test passed if the real pipeline still fails.

## v1.0 requirements

AIOS v1.0 should be considered ready only when it provides a dependable local
AIOS foundation, not merely a collection of components. The minimum bar is:

1. A stable Coordinator lifecycle with predictable startup, completion,
   timeout, and shutdown behavior.
2. Correct intent/capability/search routing for representative factual, live,
   general, and tool-oriented requests.
3. Evidence-based live search: source collection, filtering/ranking,
   deterministic validation, answerability gating, and provenance preserved into
   the answer.
4. Bounded and observable model execution, including useful failure reporting
   rather than indefinite hangs.
5. Modular prompt, model, tool, memory, and service boundaries that can be
   replaced without rewriting Coordinator.
6. A green automated test suite plus real end-to-end regression cases covering
   the critical paths.
7. A controlled local development/recovery runner, project-state documentation,
   and reproducible diagnostics.
8. No public unauthenticated shell or remote-control exposure.

The current evidence means v1.0 is **not yet met**: routing correctness and
bounded model execution need further work.

## Envisioned future expansions

These are directions, not permission to implement them ahead of stabilization:

- **Phase 4:** answer synthesis with citations/provenance, tool-aware execution,
  and autonomous multi-step reasoning with specialized agents.
- **Phase 5:** durable memory, background continuity, caching, resumable tasks,
  watchers, schedules, and recovery.
- **Phase 6:** coordinated multi-agent operating-system layer, permissions,
  events, observability, and recovery.
- **Optional integrations after stability:** travel monitoring, academic
  workflows, photography/events, NAS and storage indexing, local model
  management, app generation, and external automation.
- **Infrastructure later:** mobile workstation/remote development, independent
  CI, crash-reproduction bundles, watchdog/recovery, and authenticated remote
  control. These must plug into the controlled local-agent boundary, never
  expose a raw shell.

## Verification commands

```bat
cd C:\AIOS\Coordinator
.venv\Scripts\python.exe -m pytest -q

cd C:\AIOS
Coordinator\.venv\Scripts\python.exe -B -m unittest discover -s local_agent\tests -v
local_agent\run_agent.bat regression
```

The complete real regression may take up to 900 seconds with the default
five-minute-per-case bound. Treat its JSON output as a diagnostic artifact and
summarize it in state documentation before taking the next action.
