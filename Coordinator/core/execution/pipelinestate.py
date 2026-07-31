"""
===========================================================
AIOS Pipeline State
core/execution/pipelinestate.py

Represents ONE execution pipeline.

This is NOT the global AIOS state.

The global AIOS state (AIOSState) owns exactly one
PipelineState during a request.

Future:
AIOSState
    ├── PipelineState (foreground)
    ├── PipelineState (background job 1)
    ├── PipelineState (background job 2)
    └── ...

Version 1.0
===========================================================
"""

from dataclasses import dataclass, field

from core.execution.states import ExecutionStates


@dataclass
class PipelineState:

    # ---------------------------------
    # Pipeline
    # ---------------------------------

    current_state: ExecutionStates = ExecutionStates.START

    completed: bool = False

    history: list[str] = field(default_factory=list)

    # ---------------------------------
    # Request
    # ---------------------------------

    query: str = ""

    # ---------------------------------
    # Pipeline Outputs
    # ---------------------------------

    semantic = None

    context = None

    intent_result = None

    plan = None

    decision = None

    search_context = None

    llm_response = None

    final_response = None

    # ---------------------------------
    # Routing
    # ---------------------------------

    selected_model: str | None = None

    selected_tool: str | None = None

    # ---------------------------------
    # Diagnostics
    # ---------------------------------

    confidence: float = 0.0

    execution_order: list[str] = field(default_factory=list)