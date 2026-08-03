"""
===========================================================
AIOS Pipeline Controller

Owns the execution pipeline.

Coordinator only:
    - Boot
    - User Loop
    - Dependency Injection

PipelineController:
    - Semantic
    - Planning
    - Decision
    - Model Selection
    - Tool Selection
    - Execution
===========================================================
"""

from core.intent.classifier import IntentClassifier
from core.planner.planner import build_plan
from core.executor import execute
from core.execution.states import ExecutionStates
from core.config import DEFAULT_BACKGROUND_SUMMARY


class PipelineController:

    # --------------------------------------------------
    # Semantic Stage
    # --------------------------------------------------

    def semantic_stage(
        self,
        state,
        perception_engine,
        semantic_engine,
        context_engine,
    ):

        state.execution.current_state = ExecutionStates.SEMANTIC
        print(f"[PIPELINE] {state.execution.current_state}")

        # -------------------------
        # Perception
        # -------------------------

        state.perception = perception_engine.analyze(
            state.user_input
        )

        # -------------------------
        # Tiny Semantic LLM
        # -------------------------

        semantic = semantic_engine.understand(
            query=state.user_input,
            repository=state.repository,
            memory=state.working_memory,
        )

        state.semantic = semantic

        # -------------------------
        # Context
        # -------------------------

        state.context = context_engine.analyze(
            state.user_input,
            semantic=semantic,
        )

        # -------------------------
        # Intent
        # -------------------------

        if getattr(semantic, "intent_result", None):

            state.intent_result = semantic.intent_result

        else:

            classifier = IntentClassifier()

            state.intent_result = classifier.classify(
                state.context
            )

        state.intent = state.intent_result.intent

        return state

    # --------------------------------------------------
    # Planning Stage
    # --------------------------------------------------

    def planning_stage(self, state):

        state.execution.current_state = ExecutionStates.PLANNING
        print(f"[PIPELINE] {state.execution.current_state}")

        state.plan = build_plan(
            intent=state.intent_result,
            query=state.user_input,
            context=state.context,
            perception=state.perception,
            semantic_result=state.semantic,
        )

        return state

    # --------------------------------------------------
    # Decision Stage
    # --------------------------------------------------

    def decision_stage(
        self,
        state,
        decision_engine,
    ):

        state.execution.current_state = ExecutionStates.DECISION
        print(f"[PIPELINE] {state.execution.current_state}")

        # --------------------------------------------------
        # Decision Engine
        # --------------------------------------------------

        state.decision = decision_engine.decide(
            state.user_input,
            state.context,
            state.plan,
        )

        return state

    # --------------------------------------------------
    # Model Selection Stage
    # --------------------------------------------------

    def model_selection_stage(
        self,
        state,
        model_manager,
    ):

        state.execution.current_state = ExecutionStates.MODEL_SELECTION
        print(f"[PIPELINE] {state.execution.current_state}")

        # --------------------------------------------------
        # Model Selection
        # --------------------------------------------------

        model = model_manager.select(
            state.plan.model_capability,
            state.plan.complexity,
        )

        state.selected_model = (
            model.name
            if model
            else None
        )

        return state

    # --------------------------------------------------
    # Tool Selection Stage
    # --------------------------------------------------

    def tool_selection_stage(
        self,
        state,
        tool_manager,
    ):

        state.execution.current_state = ExecutionStates.TOOL_SELECTION
        print(f"[PIPELINE] {state.execution.current_state}")

        # --------------------------------------------------
        # Tool Selection
        # --------------------------------------------------

        selected_tool = tool_manager.select(
            state.plan.tool_capability,
        )

        state.selected_tool = (
            selected_tool.name
            if selected_tool
            else None
        )

        return state

    # --------------------------------------------------
    # Execution Stage
    # --------------------------------------------------

    def execution_stage(
        self,
        state,
        developer,
        memory,
        scheduler,
    ):

        state.execution.current_state = ExecutionStates.EXECUTION
        print(f"[PIPELINE] {state.execution.current_state}")

        state.simulation = developer.simulation

        # --------------------------------------------------
        # Execute Plan
        # --------------------------------------------------

        state = execute(state)

        # --------------------------------------------------
        # Commit Memory
        # --------------------------------------------------

        memory.commit(state)

        # --------------------------------------------------
        # Queue Background Tasks
        # --------------------------------------------------

        scheduler.queue.add_job(
            DEFAULT_BACKGROUND_SUMMARY
        )

        # --------------------------------------------------
        # Pipeline Finished
        # --------------------------------------------------

        state.execution.current_state = ExecutionStates.COMPLETE

        return state
