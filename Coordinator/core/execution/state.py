"""
===========================================================
AIOS Execution States
core/execution/states.py

Version 1.0
===========================================================
"""

from enum import Enum


class ExecutionStates(Enum):

    START = "START"

    UNDERSTAND = "UNDERSTAND"

    PLAN = "PLAN"

    MEMORY = "MEMORY"

    REPLAN = "REPLAN"

    LLM = "LLM"

    DECISION = "DECISION"

    SEARCH = "SEARCH"

    SEARCH_RETRY = "SEARCH_RETRY"

    LLM_FINAL = "LLM_FINAL"

    COMPLETE = "COMPLETE"