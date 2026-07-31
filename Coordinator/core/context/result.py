"""
===========================================================
AIOS Context Result
core/context/result.py
===========================================================

Stores semantic context produced by Context Engine.

Version 4
===========================================================
"""

from dataclasses import dataclass, field


@dataclass
class ContextResult:

    # --------------------------------------------------
    # Raw symbolic keyword matches
    # --------------------------------------------------

    matches: list = field(default_factory=list)

    # domain -> concepts
    concepts: dict = field(default_factory=dict)

    # domain -> concept -> score
    concept_scores: dict = field(default_factory=dict)

    # domain -> score
    domain_scores: dict = field(default_factory=dict)

    # --------------------------------------------------
    # Semantic Understanding
    # --------------------------------------------------

    semantic_domains: set = field(default_factory=set)

    semantic_primary_domain: str | None = None

    semantic_primary_concept: str | None = None

    # --------------------------------------------------
    # Combined Context
    # --------------------------------------------------

    @property
    def domains(self):

        symbolic = set(self.concepts.keys())

        return symbolic | self.semantic_domains

    @property
    def primary_domain(self):

        if self.semantic_primary_domain:

            return self.semantic_primary_domain

        if not self.domain_scores:

            return None

        return max(

            self.domain_scores,

            key=self.domain_scores.get

        )

    @property
    def primary_concept(self):

        if self.semantic_primary_concept:

            return self.semantic_primary_concept

        domain = self.primary_domain

        if domain is None:

            return None

        concepts = self.concept_scores.get(domain)

        if not concepts:

            return None

        return max(

            concepts,

            key=concepts.get

        )