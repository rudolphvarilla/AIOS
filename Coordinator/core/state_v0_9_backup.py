"""
AIOS State

Shared state object passed between router, workflows, models, and tools.

Future versions will be expanded for LangGraph.
"""

from dataclasses import dataclass


@dataclass
class AIOSState:

    user_input: str = ""

    intent: str = ""

    selected_model: str | None = None

    selected_tool: str | None = None

    response: str = ""

    plan: object | None = None

    working_memory = None

    simullation: bool = False

    search_results: list | None = None

    prompt: str | None = None

    decision: object | None = None