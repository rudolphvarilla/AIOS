"""
===========================================================
AIOS State
core/state.py
===========================================================

Central shared state passed throughout the AIOS execution pipeline.

Every major subsystem reads from and/or writes to this object,
allowing information to flow through AIOS without tight coupling.

Execution Flow

User
    ↓
Intent Classification
    ↓
Complexity Classification
    ↓
Planner
    ↓
Decision Engine
    ↓
Executor
    ↓
Services
    ↓
Search Pipeline
        ↓
    Filter
        ↓
    Authority
        ↓
    Ranker
        ↓
    Deduplicator
        ↓
    Extractor
        ↓
    Enricher
        ↓
    Search Context
        ↓
    Search Evaluation
    ↓
Prompt Builder
    ↓
Model
    ↓
Response

Future versions

• Search Retry
• LangGraph
• Background Tasks
• Multiple Concurrent Workflows
• Workspace Context
• Long-Term Memory
===========================================================
"""

from dataclasses import dataclass

from core.config import DEFAULT_PERSONALITY


@dataclass
class AIOSState:

    # -------------------------------------------------
    # User Request
    # -------------------------------------------------

    user_input: str = ""

    prompt: str | None = None

    # -------------------------------------------------
    # Classification
    # -------------------------------------------------

    intent: str = ""

    # -------------------------------------------------
    # Planning
    # -------------------------------------------------

    plan: object | None = None

    decision: object | None = None

    # -------------------------------------------------
    # Perception
    # -------------------------------------------------

    perception: object | None = None

    # -------------------------------------------------
    # Execution
    # -------------------------------------------------

    selected_model: str | None = None

    selected_tool: str | None = None

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    search_results: list | None = None

    search_knowledge: object | None = None

    search_summary: str | None = None

    search_context: object | None = None

    search_evaluation: object | None = None

    # -------------------------------------------------
    # Search Retry
    # -------------------------------------------------

    search_retry: bool = False

    search_retry_count: int = 0

    max_search_retry: int = 2

    # -------------------------------------------------
    # Memory
    # -------------------------------------------------

    working_memory: object | None = None

    session_memory: object | None = None

    longterm_memories: list | None = None

    longterm_summary: str | None = None

    # -------------------------------------------------
    # Repository
    # -------------------------------------------------

    repository: object | None = None

    # -------------------------------------------------
    # Time
    # -------------------------------------------------

    time: object | None = None

    # -------------------------------------------------
    # Prompt Builder
    # -------------------------------------------------

    prompt_plan: dict | None = None

    # -------------------------------------------------
    # Output
    # -------------------------------------------------

    response: str = ""

    # -------------------------------------------------
    # Development
    # -------------------------------------------------

    simulation: bool = False

    # -------------------------------------------------
    # Personality
    # -------------------------------------------------

    personality: str = DEFAULT_PERSONALITY

    # -------------------------------------------------
    # Semantic Understanding (Intent for baby model)
    # -------------------------------------------------

    semantic: dict | None = None

