"""
AIOS Router

Chooses which model or tool should handle a request.
"""

from core.intent import classify
from core.state import AIOSState
from core.planner import build_plan

from models.qwen3 import model as general_model
from models.qwen25coder import model as coding_model


def route(state: AIOSState):

    state.intent = classify(state.user_input)
    state.plan = build_plan(state.intent)

    if state.intent == "GENERAL":

        state.selected_model = state.plan.model

        state.response = general_model.ask(
            state.user_input
        )

    elif state.intent == "CODING":

        state.selected_model = state.plan.model

        state.response = coding_model.ask(
            state.user_input
        )

    elif state.intent == "DOCUMENT":

        state.selected_tool = state.plan.tool

        state.response = (
            "Document pipeline not yet connected."
        )

    return state