"""
===========================================================
AIOS Search Evaluator
core/search/evaluator.py
===========================================================

Evaluates search quality.

Two levels of evaluation

1. SearchEvidence
   Per-search-result scoring

2. SearchEvaluation
   Overall pipeline quality scoring

Version 3.0 - Phase 3.1.12 5WH validation
===========================================================
"""

from dataclasses import dataclass, field

from core.search.authority import AuthorityScorer
from core.search.relevance import RelevanceScorer
from core.config import DECISION_CONFIDENCE_THRESHOLD


@dataclass
class SearchEvidence:

    title: str
    url: str
    snippet: str
    authority: float
    relevance: float
    freshness: float
    confidence: float


@dataclass
class SearchEvaluation:

    confidence: float
    entity_count: int
    recommendation_count: int
    fact_count: int
    fivewh_score: float = 0.0
    fivewh_missing: list[str] = field(default_factory=list)
    should_retry: bool = False
    reason: str = ""


class SearchEvaluator:

    def __init__(self):
        self.authority = AuthorityScorer()
        self.relevance = RelevanceScorer()

    def evaluate(self, query, results):
        evidence = []

        for item in results:
            authority = self.authority.score(item.url)
            relevance = self.relevance.score(
                query,
                item.title,
                item.snippet,
            )
            freshness = 0.50
            confidence = authority * 0.40 + relevance * 0.60

            evidence.append(
                SearchEvidence(
                    title=item.title,
                    url=item.url,
                    snippet=item.snippet,
                    authority=authority,
                    relevance=relevance,
                    freshness=freshness,
                    confidence=confidence,
                )
            )

        return evidence

    def evaluate_context(self, context):
        entity_count = len(context.entities)
        recommendation_count = len(context.recommendations)
        fact_count = len(context.facts)
        search_confidence = context.confidence

        alignment = getattr(context, "fivewh_alignment", None)
        fivewh_score = alignment.score if alignment is not None else 1.0
        missing = alignment.missing if alignment is not None else []

        # Phase 3.1.11 measured search richness. Phase 3.1.12 now
        # requires that the retrieved material also addresses the user's
        # semantic request. This prevents a rich but tactically useless
        # search result set from being accepted solely on entity count.
        confidence = search_confidence * 0.55 + fivewh_score * 0.45
        confidence = min(1.0, max(0.0, confidence))

        if search_confidence < DECISION_CONFIDENCE_THRESHOLD:
            should_retry = True
            reason = "Low search confidence"
        elif fivewh_score < 0.70:
            should_retry = True
            reason = "5WH evidence misalignment"
        elif missing:
            should_retry = True
            reason = "Missing 5WH evidence: " + ", ".join(missing)
        else:
            should_retry = False
            reason = "Search confidence and 5WH alignment accepted"

        return SearchEvaluation(
            confidence=confidence,
            entity_count=entity_count,
            recommendation_count=recommendation_count,
            fact_count=fact_count,
            fivewh_score=fivewh_score,
            fivewh_missing=missing,
            should_retry=should_retry,
            reason=reason,
        )
