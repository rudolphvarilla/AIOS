"""
===========================================================
AIOS Search Context
core/search/context.py
===========================================================

Unified search context produced by the Search Pipeline.

Version 3
===========================================================
"""

from dataclasses import dataclass, field


@dataclass
class SearchContext:

    # -----------------------------
    # Query
    # -----------------------------

    topic: str = ""

    # -----------------------------
    # Search Summary
    # -----------------------------

    summary: str = ""

    # -----------------------------
    # Sources
    # -----------------------------

    sources: list[str] = field(default_factory=list)

    source_count: int = 0

    result_count: int = 0

    # -----------------------------
    # Knowledge
    # -----------------------------

    entities: list = field(default_factory=list)

    relations: list = field(default_factory=list)

    # -----------------------------
    # Recommendations
    # -----------------------------

    recommendations: list[str] = field(default_factory=list)

    # -----------------------------
    # Enricher
    # -----------------------------

    categories: dict = field(default_factory=dict)

    locations: list[str] = field(default_factory=list)

    attributes: list[str] = field(default_factory=list)

    facts: list[str] = field(default_factory=list)

    # -----------------------------
    # Confidence
    # -----------------------------

    confidence: float = 0.0

    # -----------------------------
    # Evaluation
    # -----------------------------

    evaluation = None
