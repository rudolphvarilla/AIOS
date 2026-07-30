"""
===========================================================
AIOS Perception Result
core/perception/result.py
===========================================================

Stores everything discovered during perception.

Produced by

    PerceptionEngine

Consumed by

    Evaluator
    Planner
    Repository
    Reflection

Version 1
===========================================================
"""

from dataclasses import dataclass, field


@dataclass
class PerceptionResult:

    # ----------------------------------------
    # Detected entities
    # ----------------------------------------

    entities: list[str] = field(default_factory=list)

    # ----------------------------------------
    # User requirements
    # ----------------------------------------

    requirements: list[str] = field(default_factory=list)

    # ----------------------------------------
    # Repository matches
    # ----------------------------------------

    repository_hits: list = field(default_factory=list)

    # ----------------------------------------
    # Overall confidence
    # ----------------------------------------

    confidence: float = 0.0

    # ----------------------------------------
    # Debug information
    # ----------------------------------------

    notes: list[str] = field(default_factory=list)