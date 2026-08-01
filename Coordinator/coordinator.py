"""
===========================================================
AIOS Coordinator v0.9
===========================================================

Artificial Intelligence Operating System

Central execution engine responsible for:

• Intent Classification
• Complexity Classification
• Execution Planning
• Decision Engine
• Capability Routing
• Model Selection
• Tool Selection
• Service Selection
• Provider Selection
• Memory Management
• Background Job Scheduling
• Performance Monitoring
• Developer Simulation Mode

This module orchestrates every AIOS subsystem.

Future Versions:
- Automatic Search Decision Expansion
- Long-Term Memory (Qdrant)
- Knowledge Graph (Graphify)
- AnythingLLM Integration
- Workspace Context System
- AIOS.md User Profile
- Translation Service
- Autonomous Scheduler
- Sentinel Monitoring
===========================================================
"""

from core.state import AIOSState

from core.planner.planner import build_plan
from core.executor import execute
from core.performance import PerformanceMonitor
from core.commands.handler import handle_command
from core.recall.engine import recall
from core.system.boot import AIOSBoot
from core.system.version import version
from core.config import (PROMPT_PREVIEW_LIMIT, TOKEN_ESTIMATE_DIVISOR, DEFAULT_BACKGROUND_SUMMARY)
from core.perception.engine import PerceptionEngine
from core.output.presenter import Presenter

from core.context.engine import ContextEngine
from core.intent.classifier import IntentClassifier
from core.intent.llm_understanding import SemanticUnderstanding

from core.execution.pipelinestate import PipelineState
from core.execution.states import ExecutionStates
from core.execution.pipeline_controller import PipelineController


def main():

    print("=" * 60)
    print(f"AIOS Coordinator v{version()}")
    print("=" * 60)
    print("Type /exit to close AIOS.")
    print()

    boot = AIOSBoot()

    services = boot.initialize()

    repository = services.repository

    print("\n===== Loading Repository Modules =====")
    print(f"Memory Module        : {type(repository.memory).__name__}")
    print(f"Knowledge Module     : {type(repository.knowledge).__name__}")
    print(f"Event Module         : {type(repository.events).__name__}")
    print(f"Relationship Module  : {type(repository.relationships).__name__}")
    print(f"Watcher Module       : {type(repository.watchers).__name__}")

    memory = repository.memory

    scheduler = services.scheduler

    developer = services.developer

    model_manager = services.model_manager

    tool_manager = services.tool_manager

    decision_engine = services.decision_engine

    time_manager = services.time

    perception_engine = PerceptionEngine()

    context_engine = ContextEngine()

    semantic_engine = SemanticUnderstanding(model_manager)

    pipeline = PipelineController()

    while True:

        state = AIOSState()

        state.execution = PipelineState(query="")
        state.execution.current_state = ExecutionStates.START

        state.working_memory = memory
        state.repository = repository
        state.time = time_manager

        perf = PerformanceMonitor()

        state.user_input = input("You: ").strip()

        state.execution.query = state.user_input

        # Ignore empty input
        if not state.user_input:
            continue

        # Exit command
        result = handle_command(
            state.user_input,
            memory,
            state,
            developer,
            scheduler
        )

        context = recall(
            state.user_input,
            memory
        )

        if result == "EXIT":

            print("\nAIOS shutting down...")

            break

        elif result == "CONTINUE":

            continue

        if developer.enabled and context:

            print("\n---- RECALL ENGINE ----")

            print(context)

        # -------------------------
        # Semantic Analysis
        # -------------------------

        perf.start("Semantic Analysis")

        state = pipeline.semantic_stage(
            state,
            perception_engine,
            semantic_engine,
            context_engine,
        )

        perf.stop("Semantic Analysis")

        # -------------------------
        # Planning Stage
        # -------------------------

        perf.start("Planning")

        state = pipeline.planning_stage(state)

        perf.stop("Planning")

        # -------------------------
        # Decision Stage
        # -------------------------

        perf.start("Decision")

        state = pipeline.decision_stage(
            state,
            decision_engine,
            model_manager,
            tool_manager,
        )

        perf.stop("Decision")

        # -------------------------
        # Execution Stage
        # -------------------------

        perf.start("Execution")

        state = pipeline.execution_stage(
            state,
            developer,
            memory,
            scheduler,
        )

        perf.stop("Execution")

        # -------------------------
        # Output
        # -------------------------

        Presenter().present(
            state=state,
            developer=developer,
            memory=memory,
            scheduler=scheduler,
            performance=perf,
        )

if __name__ == "__main__":
    main()