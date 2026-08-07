"""
===========================================================
AIOS Search Context
core/search/context.py
===========================================================

Unified search context produced by the Search Pipeline.

Version 3.2 - Phase 3.1.14 answerability validation
===========================================================
"""

from dataclasses import dataclass, field


@dataclass
class SearchContext:

    topic: str = ""
    summary: str = ""

    sources: list[str] = field(default_factory=list)
    source_count: int = 0
    result_count: int = 0

    entities: list = field(default_factory=list)
    relations: list = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)

    categories: dict = field(default_factory=dict)
    locations: list[str] = field(default_factory=list)
    attributes: list[str] = field(default_factory=list)
    facts: list[str] = field(default_factory=list)

    # Phase 3.1.12 5WH semantic validation
    fivewh = None
    fivewh_alignment = None

    # Phase 3.1.14 answerability validation
    answerability = None

    confidence: float = 0.0
    evaluation = None
