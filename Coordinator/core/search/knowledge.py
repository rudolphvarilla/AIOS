"""
===========================================================
AIOS Search Knowledge
core/search/knowledge.py
===========================================================

Contains the semantic knowledge extracted from search.

Version 2.0
===========================================================
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------
# Entity
# ---------------------------------------------------------

@dataclass
class SearchEntity:

    name: str

    entity_type: str

    source: str


# ---------------------------------------------------------
# Relation
# ---------------------------------------------------------

@dataclass
class SearchRelation:

    source: str

    relation: str

    target: str


# ---------------------------------------------------------
# Search Knowledge
# ---------------------------------------------------------

@dataclass
class SearchKnowledge:

    entities: list[SearchEntity] = field(default_factory=list)

    relations: list[SearchRelation] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)

    categories: dict = field(default_factory=dict)

    locations: list[str] = field(default_factory=list)

    attributes: list[str] = field(default_factory=list)

    facts: list[str] = field(default_factory=list)