# AIOS Project Roadmap

## Project
AIOS (Artificial Intelligence Operating System) is being developed as a modular AI operating system and personal AI platform. The architecture is built incrementally, with deterministic orchestration, semantic understanding, evidence-grounded search, iterative context construction, and eventually autonomous operation.

## Current Goal
**Phase 3.2 — Connect and harden Phase 3.1 into actual AIOS execution.**

Phase 3.1 established semantic context, deterministic evidence, search processing, answerability, and the iterative Builder/Judge/Manager foundation. Phase 3.2 closes the remaining integration gaps between those components and the real AIOS execution path.

### 3.2 workflow
1. Audit the actual Phase 3.1 → Coordinator → Prompt Builder → LLM path.
2. Identify where Phase 3.1 outputs are bypassed, lost, flattened, or not consumed.
3. Create a **Stem** for each important proposed fix.
4. Test the Stem against the real AIOS execution path.
5. **Prune** a Stem if it does not solve the identified problem.
6. If successful, **integrate** the Stem into the Current Goal implementation.
7. Run the relevant regression/integration tests.
8. After every successful test gate, update Project/Current Goal/Stem state documentation before beginning the next task.

### 3.2.0v2
Documentation reconciliation and project-state correction based on the post-3.1.18 `main` baseline.

### 3.2.1v2
Re-verify the local development-agent capability established during the original 3.2.1 work, including access to `C:\AIOS\Coordinator`, the project virtual environment, Python, Git, and the full regression suite.

### 3.2.2v2
Audit and close the real integration gaps between Phase 3.1 and the actual AIOS execution pipeline. Do not redesign working Phase 3.1 components without evidence that a redesign is necessary.

## Stem
A **Stem** is a temporary experimental implementation used when an important function or integration point needs to be inserted, changed, or tested. A Stem is not part of the Current Goal until it demonstrates that it solves the target problem.

### Stem lifecycle
`Current Goal → Stem → Test → Prune OR Integrate → Regression → Documentation update`

## Added Features / Later Infrastructure
These are intentionally outside the immediate Phase 3.2 implementation unless a dependency is discovered:

- Mobile workstation / remote development capability, to allow AIOS development and recovery from a mobile device when the local Windows machine is unavailable.
- Local development agent.
- Independent CI/test execution.
- Crash capture and reproducible crash bundles.
- AIOS watchdog and recovery infrastructure.
- Remote development/control layer.

The **Mobile workstation** is planned **after AIOS stabilization**, rather than being introduced into the current Phase 3.2 search/context work.

## Phase 3.3 — Actual AIOS Validation and Development Output Refactor
After Phase 3.2 is integrated and stable, Phase 3.3 will test the completed implementations through the actual AIOS execution path. It will also refactor development/debug output so that Coordinator remains a coordinator rather than becoming a development-output container, and will update/refactor `/help` to reflect the expanded system functionality.

## Phase 4 — Autonomous Reasoning
Phase 4 builds on validated Phase 3 context and execution integration to introduce autonomous multi-step reasoning and agent cooperation. Planned capabilities include research, memory, travel, coding, and other specialized agents coordinated by AIOS.

## Phase 5 — AIOS Operating System
Long-term autonomous operation: background scheduler, watcher agents, calendar/travel/email monitoring, NAS indexing, photo/project organization, self-maintaining memory, and continuous background reasoning.

## State Discipline
`main` is the current post-3.1.18 development baseline. The `backup/phase-3.1.18-main-2026-08-11` branch is the safety snapshot. Experimental changes use Stems. The Current Goal is updated only after successful test gates and before proceeding to the next task.
