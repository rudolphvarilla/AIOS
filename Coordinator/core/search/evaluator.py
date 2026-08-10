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

Phase 3.1.14 adds answerability validation so topical relevance and
5WH alignment cannot by themselves approve an unusable answer.
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
    answerability_score: float = 1.0
    answerability_missing: list[str] = field(default_factory=list)
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
        fivewh_missing = alignment.missing if alignment is not None else []

        answerability = getattr(context, "answerability", None)
        answerability_available = answerability is not None
        answerability_score = (
            answerability.score if answerability_available else 1.0
        )
        answerability_missing = (
            answerability.missing if answerability_available else []
        )

        # Confidence now reflects three different questions:
        #
        # 1. Is the search result set rich enough?
        # 2. Does it align with the requested 5WH semantics?
        # 3. Does it contain answer-bearing evidence?
        confidence = (
            search_confidence * 0.35
            + fivewh_score * 0.30
            + answerability_score * 0.35
        )
        confidence = min(1.0, max(0.0, confidence))

        # Answerability is the decisive gate when the context builder has
        # validated explicit answer-bearing evidence. Sparse-result context
        # confidence is a richness signal and must not force another search
        # after a complete answer has already been validated. If answerability
        # is unavailable, the legacy search-confidence threshold remains the
        # fallback gate. 5WH gaps remain retry-worthy only when they materially
        # reduce alignment or the evidence is not otherwise answer-bearing.
        if answerability_available and answerability_score < 0.60:
            should_retry = True
            reason = "Insufficient answer-bearing evidence"
            if answerability_missing:
                reason += ": " + ", ".join(answerability_missing)
        elif fivewh_score < 0.70:
            should_retry = True
            reason = "5WH evidence misalignment"
        elif answerability_available and fivewh_missing and answerability_score < 1.0:
            should_retry = True
            reason = "Missing 5WH evidence: " + ", ".join(fivewh_missing)
        elif not answerability_available and search_confidence < DECISION_CONFIDENCE_THRESHOLD:
            should_retry = True
            reason = "Low search confidence"
        else:
            should_retry = False
            reason = "Search confidence, 5WH alignment, and answerability accepted"

        return SearchEvaluation(
            confidence=confidence,
            entity_count=entity_count,
            recommendation_count=recommendation_count,
            fact_count=fact_count,
            fivewh_score=fivewh_score,
            fivewh_missing=fivewh_missing,
            answerability_score=answerability_score,
            answerability_missing=answerability_missing,
            should_retry=should_retry,
            reason=reason,
        )
