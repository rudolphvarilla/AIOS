"""
===========================================================
AIOS Search Knowledge
core/search/knowledge.py
===========================================================

Contains semantic knowledge and source-grounded evidence extracted
from search.

Version 2.1
===========================================================
"""

from dataclasses import dataclass, field

from core.search.evidence import SearchFact


# ---------------------------------------------------------
# Entity
# ---------------------------------------------------------

@dataclass
class SearchEntity:

    name: str

    entity_type: str

    source: str


# ---------------------------------------------------------
# Fact
# ---------------------------------------------------------

@dataclass
class SearchFact:
    """A deterministic fact candidate with explicit provenance.

    The extractor never invents a value. ``evidence`` is copied from the
    retrieved title/snippet and ``source`` identifies the result it came from.
    """

    subject: str
    predicate: str
    value: str
    source: str
    evidence: str
    fact_type: str = "statement"
    confidence: float = 1.0

    def render(self) -> str:
        return (
            f"{self.subject} {self.predicate} {self.value} "
            f"[source: {self.source}]"
        )


# ---------------------------------------------------------
# Relation
# ---------------------------------------------------------

@dataclass
class SearchRelation:

    source: str

    relation: str

    target: str

    @property
    def relationship(self) -> str:
        """Backward-compatible alias for the legacy field name."""
        return self.relation


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

    # Source-grounded evidence. This is intentionally open-world: the
    # extractor may introduce terminology that was never present in a manual
    # domain registry.
    facts: list[SearchFact] = field(default_factory=list)
