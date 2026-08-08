"""
===========================================================
AIOS Context Engine
core/context/engine.py
===========================================================

Builds semantic context for AIOS.

Sources
-------
1. Semantic Understanding (preferred)
2. Keyword Matcher (fallback / enrichment)

===========================================================
"""

from collections import defaultdict

from core.context.result import ContextResult
from core.keywords.matcher import KeywordMatcher
from core.context.sense import SenseResolver


class ContextEngine:

    def __init__(self):
        self.matcher = KeywordMatcher()
        self.sense_resolver = SenseResolver()

    # =====================================================
    # Main Analysis
    # =====================================================

    def analyze(

        self,

        text,

        semantic=None,

    ):

        result = ContextResult()

        if semantic is not None:
            result.semantic_domains = set(semantic.domains)
            if semantic.domains:
                result.semantic_primary_domain = semantic.domains[0]
            if semantic.concepts:
                result.semantic_primary_concept = semantic.concepts[0]

        # ------------------------------------------
        # STEP 2
        # Keyword enrichment
        # ------------------------------------------

        matches = self.matcher.match(text)

        matches = self.sense_resolver.resolve(
            text,
            matches,
            semantic=semantic,
        )

        result.matches = matches

        concepts = defaultdict(set)
        concept_scores = defaultdict(lambda: defaultdict(float))
        domain_scores = defaultdict(float)

        for item in matches:
            domain = item["domain"]
            concept = item["concept"]
            confidence = item.get("confidence", 1.0)

            concepts[domain].add(concept)
            concept_scores[domain][concept] += confidence
            domain_scores[domain] += confidence

        for domain, values in concepts.items():
            existing = set(result.concepts.get(domain, []))
            existing.update(values)
            result.concepts[domain] = sorted(existing)

        result.concept_scores = {
            domain: dict(scores)
            for domain, scores in concept_scores.items()
        }
        result.domain_scores = dict(domain_scores)

        return result
