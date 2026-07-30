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


class ContextEngine:

    def __init__(self):

        self.matcher = KeywordMatcher()

    # =====================================================
    # Main Analysis
    # =====================================================

    def analyze(

        self,

        text,

        semantic=None,

    ):

        result = ContextResult()

        # ------------------------------------------
        # STEP 1
        # Seed context from semantic understanding
        # ------------------------------------------

        if semantic is not None:

            # domains

            if hasattr(semantic, "domains"):

                result.domains = set(semantic.domains)

            # concepts

            if hasattr(semantic, "concepts"):

                result.concepts = semantic.concepts

            # primary selections

            result.primary_domain = getattr(

                semantic,

                "primary_domain",

                None,

            )

            result.primary_concept = getattr(

                semantic,

                "primary_concept",

                None,

            )

        # ------------------------------------------
        # STEP 2
        # Keyword enrichment
        # ------------------------------------------

        matches = self.matcher.match(text)

        result.matches = matches

        concepts = defaultdict(set)

        concept_scores = defaultdict(

            lambda: defaultdict(float)

        )

        domain_scores = defaultdict(float)

        for item in matches:

            domain = item["domain"]

            concept = item["concept"]

            confidence = item.get(

                "confidence",

                1.0,

            )

            concepts[domain].add(concept)

            concept_scores[domain][concept] += confidence

            domain_scores[domain] += confidence

        # ------------------------------------------
        # Merge semantic concepts with keyword concepts
        # ------------------------------------------

        for domain, values in concepts.items():

            existing = set(

                result.concepts.get(

                    domain,

                    [],

                )

            )

            existing.update(values)

            result.concepts[domain] = sorted(existing)

        result.concept_scores = {

            domain: dict(scores)

            for domain, scores

            in concept_scores.items()

        }

        result.domain_scores = dict(domain_scores)

        # ------------------------------------------
        # STEP 3
        # If semantic did not determine primary domain,
        # use keyword confidence.
        # ------------------------------------------

        if result.primary_domain is None:

            if domain_scores:

                result.primary_domain = max(

                    domain_scores,

                    key=domain_scores.get,

                )

        # ------------------------------------------
        # STEP 4
        # Populate domain list
        # ------------------------------------------

        if hasattr(result, "domains"):

            result.domains.update(

                result.concepts.keys()

            )

        else:

            result.domains = set(

                result.concepts.keys()

            )

        # ------------------------------------------
        # STEP 5
        # Resolve primary concept if still empty
        # ------------------------------------------

        if (

            result.primary_concept is None

            and result.primary_domain is not None

        ):

            domain = result.primary_domain

            scores = result.concept_scores.get(

                domain,

                {},

            )

            if scores:

                result.primary_concept = max(

                    scores,

                    key=scores.get,

                )

        return result