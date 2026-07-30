"""
===========================================================
AIOS Semantic Result
core/semantics/result.py
===========================================================

Structured output produced by the Tiny Semantic Model.

This object becomes the bridge between

User Input
        ↓
Tiny Semantic Model
        ↓
Context Engine
        ↓
Planner
        ↓
Decision Engine

Version 1.0
===========================================================
"""

from dataclasses import dataclass, field


@dataclass
class SemanticResult:

    # -------------------------------------------------
    # Semantic Understanding
    # -------------------------------------------------

    domains: list[str] = field(default_factory=list)

    concepts: list[str] = field(default_factory=list)

    entities: list[str] = field(default_factory=list)

    requirements: list[str] = field(default_factory=list)

    # -------------------------------------------------
    # Planning Hints
    # -------------------------------------------------

    complexity: str = "LOW"

    confidence: float = 0.0

    execution_order: list[str] = field(default_factory=list)

    # -------------------------------------------------
    # Search Understanding
    # -------------------------------------------------

    normalized_query: str = ""

    search_query: str = ""

    search_intent: str = ""

    needs_search: bool = False

    ambiguity: float = 0.0

    # -------------------------------------------------
    # Capability Hints
    # -------------------------------------------------

    requires_search: bool = False

    requires_code: bool = False

    requires_memory: bool = False

    requires_repository: bool = False

    requires_vision: bool = False

    requires_image_generation: bool = False

    # -------------------------------------------------
    # Intent (future)
    # -------------------------------------------------

    intent_result = None

    # -------------------------------------------------

    @classmethod
    def empty(cls):

        return cls()

    # -------------------------------------------------

    @classmethod
    def from_dict(cls, data):

        obj = cls()

        for key, value in data.items():

            if hasattr(obj, key):

                setattr(obj, key, value)

        return obj

    # -------------------------------------------------

    def to_dict(self):

        return {

            "domains": self.domains,

            "concepts": self.concepts,

            "entities": self.entities,

            "requirements": self.requirements,

            "complexity": self.complexity,

            "confidence": self.confidence,

            "execution_order": self.execution_order,

            "requires_search": self.requires_search,

            "requires_code": self.requires_code,

            "requires_memory": self.requires_memory,

            "requires_repository": self.requires_repository,

            "requires_vision": self.requires_vision,

            "requires_image_generation": self.requires_image_generation,

            "normalized_query": self.normalized_query,
            "search_query": self.search_query,
            "search_intent": self.search_intent,
            "needs_search": self.needs_search,
            "ambiguity": self.ambiguity,

        }