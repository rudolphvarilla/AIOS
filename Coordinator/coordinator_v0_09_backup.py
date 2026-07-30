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

from core.intent import classify
from core.planner import build_plan
from core.executor import execute
from core.performance import PerformanceMonitor
from core.commands.handler import handle_command
from core.recall.engine import recall
from core.system.boot import AIOSBoot
from core.system.version import version

def main():

    print("=" * 60)
    print(f"AIOS Coordinator v{version()}")
    print("=" * 60)
    print("Type /exit to close AIOS.")
    print()

    boot = AIOSBoot()

    system = boot.initialize()

    memory = system.memory

    scheduler = system.scheduler

    developer = system.developer

    model_manager = system.model_manager

    tool_manager = system.tool_manager

    decision_engine = system.decision_engine

    while True:

        state = AIOSState()

        state.working_memory = memory

        perf = PerformanceMonitor()

        state.user_input = input("You: ").strip()

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
        # Intent Classification
        # -------------------------

        perf.start("Intent Classification")

        state.intent = classify(state.user_input)

        perf.stop("Intent Classification")

        # -------------------------
        # Execution Planning
        # -------------------------

        perf.start("Execution Planning")

        state.plan = build_plan(
            state.intent,
            state.user_input
        )

        perf.stop("Execution Planning")

        # -------------------------
        # Decision Engine
        # -------------------------

        state.decision = decision_engine.decide(
            state.user_input
        )

        # -------------------------
        # Model Selection
        # -------------------------

        selected_model = model_manager.select(
            state.plan.model_capability,
            state.plan.complexity,
        )

        if selected_model is not None:

            state.selected_model = selected_model.name

        else:

            state.selected_model = None

        # -------------------------
        # Tool Selection
        # -------------------------

        selected_tool = tool_manager.select(
            state.plan.tool_capability,
        )

        if selected_tool is not None:

            state.selected_tool = selected_tool.name

        else:

            state.selected_tool = None

        # -------------------------
        # Execution
        # -------------------------

        perf.start("Execution")

        state.simulation = developer.simulation

        state = execute(state)

        memory.commit(state)

        scheduler.queue.add_job(
            "Summarize previous response"
        )

        perf.stop("Execution")

        # -------------------------
        # Output
        # -------------------------

        print("\n----- RESPONSE -----")

        print(state.response)

        print()

        if developer.enabled:

            print("\n----- ROUTING RESULT -----")

            print(f"Simulation       : {'ON' if state.simulation else 'OFF'}")
            print(f"Intent           : {state.intent}")
            print(f"Complexity       : {state.plan.complexity}")
            print(f"Model            : {state.selected_model}")
            print(f"Model Capability : {state.plan.model_capability}")
            print(f"Tool Capability  : {state.plan.tool_capability}")
            print(f"Use Search       : {state.decision.use_search}")
            print(f"Background       : {state.decision.background}")
            print(f"Decision         : {state.decision.reasoning}")

            if state.search_results:
                print(f"Search Results   : {len(state.search_results)}")

            # -------------------------
            # Prompt Inspector
            # -------------------------

            if state.prompt:

                print("\n----- PROMPT INSPECTOR -----")

                prompt_length = len(state.prompt)

                estimated_tokens = prompt_length // 4

                print(f"Prompt Length   : {prompt_length} characters")
                print(f"Estimated Tokens: ~{estimated_tokens}")

                print("\n----- PROMPT PREVIEW -----")

                preview = state.prompt[:1200]

                print(preview)

                if prompt_length > 1200:

                    print("\n... (truncated)")

            print("\n----- EXECUTION PLAN -----")

            print(state.plan)

            print("\n---- WORKING MEMORY ----")

            print(memory.working)

            print("\n---- SESSION MEMORY ----")

            for item in memory.session.history:
                print(item)

            print("\n---- BACKGROUND QUEUE ----")

            print(f"Pending Jobs : {scheduler.queue.count()}")

            for i, job in enumerate(scheduler.queue.list_jobs(), start=1):

                print()

                print(f"[{i}]")

                print(f"Status      : {job.status}")

                print(f"Description : {job.description}")

                print(f"Created     : {job.timestamp}")

            perf.report()


if __name__ == "__main__":
    main()