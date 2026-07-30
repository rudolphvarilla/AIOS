"""
===========================================================
AIOS Planner Schema
core/planner/planner_schema.py
===========================================================

Canonical execution plan used internally by AIOS.

The planner (Tiny Reasoner) converts user requests into
PlannerPlan objects.

Every downstream component consumes this object.

Coordinator
Search
Memory
Repository
Executor
Background Scheduler

Version 1.0
===========================================================
"""

from dataclasses import dataclass, field


# =========================================================
# Planner Entity
# =========================================================

@dataclass
class PlannerEntity:

    text: str

    label: str

    confidence: float = 1.0


# =========================================================
# Planner Tool
# =========================================================

@dataclass
class PlannerTool:

    name: str

    capability: str


# =========================================================
# Planner Plan
# =========================================================

@dataclass
class PlannerPlan:

    # -----------------------------
    # High-level intent
    # -----------------------------

    goal: str = ""

    intent: str = "GENERAL"

    complexity: str = "LOW"

    # -----------------------------
    # Search
    # -----------------------------

    search_query: str = ""

    use_search: bool = False

    # -----------------------------
    # Memory
    # -----------------------------

    use_memory: bool = False

    # -----------------------------
    # Repository
    # -----------------------------

    use_repository: bool = False

    # -----------------------------
    # External tools
    # -----------------------------

    use_tools: bool = False

    tools: list[PlannerTool] = field(default_factory=list)

    # -----------------------------
    # Background
    # -----------------------------

    use_background: bool = False

    background_description: str = ""

    # -----------------------------
    # Extracted entities
    # -----------------------------

    entities: list[PlannerEntity] = field(default_factory=list)

    # -----------------------------
    # Planner confidence
    # -----------------------------

    confidence: float = 1.0

    reasoning: str = ""

    execution_order: list[str] = field(default_factory=list)