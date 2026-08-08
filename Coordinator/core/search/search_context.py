"""
===========================================================
AIOS Search Context Builder
core/search/search_context.py
===========================================================

Builds the unified SearchContext object.

Version 4.4 - deterministic fact records and fact-aware answerability
===========================================================
"""

from core.search.context import SearchContext
from core.search.fivewh_validator import FiveWHValidator
from core.search.fact_aware_answerability import FactAwareAnswerabilityValidator


class SearchContextBuilder:

    def __init__(self):
        self.fivewh_validator = FiveWHValidator()
        self.answerability_validator = FactAwareAnswerabilityValidator()

    def build(
        self,
        query,
        results,
        knowledge,
        summary,
        fivewh=None,
    ):
        confidence = 0.40

        confidence += min(len(results), 10) * 0.04
        confidence += min(len(knowledge.entities), 20) * 0.01
        confidence += min(len(knowledge.relations), 20) * 0.02

        # Phase 3.2: bounded source-grounded evidence contribution.
        confidence += min(len(knowledge.facts), 10) * 0.02

        confidence = min(confidence, 1.0)

        context = SearchContext(
            topic=query,
            summary=summary,
            sources=[r.url for r in results[:5]],
            source_count=min(len(results), 5),
            entities=knowledge.entities,
            relations=knowledge.relations,
            recommendations=knowledge.recommendations,
            categories=knowledge.categories,
            locations=knowledge.locations,
            attributes=knowledge.attributes,
            facts=knowledge.facts,
            fact_records=knowledge.fact_records,
            confidence=confidence,
            result_count=len(results),
        )

        context.fivewh = fivewh
    
        if fivewh is not None:
            context.fivewh_alignment = self.fivewh_validator.validate(
                fivewh,
                context,
            )

            context.answerability = self.answerability_validator.validate(
                fivewh,
                results,
                summary=summary,
                facts=knowledge.fact_records,
            )

        return context
