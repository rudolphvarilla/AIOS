"""
===========================================================
AIOS Context Result
core/context/result.py
===========================================================

Stores semantic context produced by Context Engine.

Version 3
===========================================================
"""

from dataclasses import dataclass, field


@dataclass
class ContextResult:

    # Raw keyword matches
    matches: list = field(default_factory=list)

    # domain -> concepts
    concepts: dict = field(default_factory=dict)

    # NEW
    # domain -> concept -> score
    concept_scores: dict = field(default_factory=dict)

    # domain -> score
    domain_scores: dict = field(default_factory=dict)

    @property
    def domains(self):

        return set(self.concepts.keys())

    @property
    def primary_domain(self):

        if not self.domain_scores:

            return None

        return max(
            self.domain_scores,
            key=self.domain_scores.get
        )

    @property
    def primary_concept(self):

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