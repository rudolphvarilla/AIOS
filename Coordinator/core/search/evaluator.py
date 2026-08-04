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

Responsibilities

• Authority
• Relevance
• Freshness
• Confidence
• Retry decision

Version 2.0
===========================================================
"""

from dataclasses import dataclass

from core.search.authority import AuthorityScorer
from core.search.relevance import RelevanceScorer
from core.config import DECISION_CONFIDENCE_THRESHOLD

# =========================================================
# Individual Search Result
# =========================================================

@dataclass
class SearchEvidence:

    title: str

    url: str

    snippet: str

    authority: float

    relevance: float

    freshness: float

    confidence: float


# =========================================================
# Whole Search Evaluation
# =========================================================

@dataclass
class SearchEvaluation:

    confidence: float

    entity_count: int

    recommendation_count: int

    fact_count: int

    should_retry: bool

    reason: str


# =========================================================
# Evaluator
# =========================================================

class SearchEvaluator:

    def __init__(self):

        self.authority = AuthorityScorer()

        self.relevance = RelevanceScorer()

    # -----------------------------------------------------
    # Evaluate individual search results
    # -----------------------------------------------------

    def evaluate(

        self,

        query,

        results,

    ):

        evidence = []

        for item in results:

            authority = self.authority.score(item.url)

            relevance = self.relevance.score(

                query,

                item.title,

                item.snippet,

            )

            freshness = 0.50

            confidence = (

                authority * 0.40

                +

                relevance * 0.60

            )

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

    # -----------------------------------------------------
    # Evaluate final search context
    # -----------------------------------------------------

    def evaluate_context(

        self,

        context,

    ):

        entity_count = len(context.entities)

        recommendation_count = len(context.recommendations)

        fact_count = len(context.facts)

        confidence = context.confidence

        # -------------------------------------------------
        # Confidence Gate
        # -------------------------------------------------

        if confidence >= 0.80:

            should_retry = False

            reason = "Confidence accepted"

        else:

            should_retry = True

            reason = "Low confidence"

        return SearchEvaluation(

            confidence=confidence,

            entity_count=entity_count,

            recommendation_count=recommendation_count,

            fact_count=fact_count,

            should_retry=should_retry,

            reason=reason,

        )