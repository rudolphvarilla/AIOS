"""
=========================================================
AIOS Execution States
=========================================================

Central execution pipeline state definitions.

Phase 3 Architecture
=========================================================
"""

class ExecutionStates:

    START = "START"

    PERCEPTION = "PERCEPTION"

    SEMANTIC = "SEMANTIC"

    CONTEXT = "CONTEXT"

    INTENT = "INTENT"

    PLANNING = "PLANNING"

    DECISION = "DECISION"

    MODEL_SELECTION = "MODEL_SELECTION"

    TOOL_SELECTION = "TOOL_SELECTION"

    EXECUTION = "EXECUTION"

    MEMORY_COMMIT = "MEMORY_COMMIT"

    BACKGROUND_QUEUE = "BACKGROUND_QUEUE"

    PRESENTATION = "PRESENTATION"

    COMPLETE = "COMPLETE"

    ERROR = "ERROR"