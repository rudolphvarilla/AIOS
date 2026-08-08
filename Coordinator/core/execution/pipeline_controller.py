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

from concurrent.futures import ThreadPoolExecutor

from core.intent.classifier import IntentClassifier
from core.planner.planner import build_plan
from core.executor import execute
from core.execution.states import ExecutionStates
from core.config import (DEFAULT_BACKGROUND_SUMMARY, DECISION_CONFIDENCE_THRESHOLD,)
from core.semantics.fivewh import FiveWHUnderstanding


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

        state.perception = perception_engine.analyze(
            state.user_input
        )

        # --------------------------------------------------
        # Parallel semantic understanding
        # --------------------------------------------------
        # The normal semantic model determines routing/search hints.
        # 5WH independently determines what the user needs from search.
        # They are deliberately kept separate so one model cannot silently
        # manufacture the validation target used by the other.

        fivewh_engine = FiveWHUnderstanding(
            semantic_engine.model_manager
        )

        with ThreadPoolExecutor(max_workers=2) as executor_pool:

            semantic_future = executor_pool.submit(
                semantic_engine.understand,
                query=state.user_input,
                repository=state.repository,
                memory=state.working_memory,
            )

            fivewh_future = executor_pool.submit(
                fivewh_engine.understand,
                query=state.user_input,
                repository=state.repository,
                memory=state.working_memory,
            )

            semantic = semantic_future.result()
            fivewh = fivewh_future.result()

        state.semantic = semantic
        state.fivewh = fivewh

        print("\n===== 5WH =====")
        print(f"Who   : {fivewh.who}")
        print(f"What  : {fivewh.what}")
        print(f"When  : {fivewh.when}")
        print(f"Where : {fivewh.where}")
        print(f"Why   : {fivewh.why}")
        print(f"How   : {fivewh.how}")
        print(f"Confidence : {fivewh.confidence:.2f}")

        state.context = context_engine.analyze(
            state.user_input,
            semantic=semantic,
        )

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

        state.decision = decision_engine.decide(
            state.user_input,
            state.context,
            state.plan,
        )

        confidence = getattr(
            state.intent_result,
            "confidence",
            0.0,
        )

        if confidence < DECISION_CONFIDENCE_THRESHOLD:
            print(
                f"[DECISION] Confidence below threshold."
                f"({confidence:2f}). Retrying decision."
            )
            state.decision = decision_engine.decide(
                state.user_input,
                state.context,
                state.plan,
                retry=True,
            )
        else:
            print(
                f"[DECISION] Confidence accepted "
                f"({confidence:.2f})"
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

        state = execute(state)

        memory.commit(state)

        scheduler.queue.add_job(
            DEFAULT_BACKGROUND_SUMMARY
        )

        state.execution.current_state = ExecutionStates.COMPLETE

        return state
