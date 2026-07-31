"""
===========================================================
AIOS Pipeline Controller

Coordinates execution stages.

Coordinator only controls lifecycle.

PipelineController controls execution.
===========================================================
"""

from core.intent.classifier import IntentClassifier
from core.planner.planner import build_plan
from core.execution.states import ExecutionStates

class PipelineController:

    def semantic_stage(
        self,
        state,
        perception_engine,
        semantic_engine,
        context_engine,
    ):

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

    def planning_stage(self, state):

        state.execution.current_state = ExecutionStates.PLANNING

        state.plan = build_plan(
            intent=state.intent_result,
            query=state.user_input,
            context=state.context,
            perception=state.perception,
            semantic_result=state.semantic,
        )

        return state

