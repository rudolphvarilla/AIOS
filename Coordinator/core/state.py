"""
===========================================================
AIOS State
core/state.py
===========================================================

Central shared state passed throughout the AIOS execution pipeline.

Version 1.1 - Phase 3.1.12 5WH semantic validation
===========================================================
"""

from dataclasses import dataclass
from core.config import DEFAULT_PERSONALITY


@dataclass
class AIOSState:

    user_input: str = ""
    prompt: str | None = None

    intent: str = ""

    plan: object | None = None
    decision: object | None = None

    perception: object | None = None

    selected_model: str | None = None
    selected_tool: str | None = None

    search_results: list | None = None
    search_knowledge: object | None = None
    search_summary: str | None = None
    search_context: object | None = None
    search_evaluation: object | None = None

    search_retry: bool = False
    search_retry_count: int = 0
    max_search_retry: int = 2

    working_memory: object | None = None
    session_memory: object | None = None
    longterm_memories: list | None = None
    longterm_summary: str | None = None

    repository: object | None = None
    time: object | None = None

    prompt_plan: dict | None = None

    response: str = ""

    simulation: bool = False
    personality: str = DEFAULT_PERSONALITY

    # Tiny semantic understanding result.
    semantic: dict | None = None

    # Phase 3.1.12 query-intent validation target.
    fivewh: object | None = None
