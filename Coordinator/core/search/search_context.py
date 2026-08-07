"""
===========================================================
AIOS Search Context Builder
core/search/search_context.py
===========================================================

Builds the unified SearchContext object.

Version 4.1
===========================================================
"""

from core.search.context import SearchContext


class SearchContextBuilder:

    def build(self, query, results, knowledge, summary):
        confidence = 0.40

        confidence += min(len(results), 10) * 0.04
        confidence += min(len(knowledge.entities), 20) * 0.01
        confidence += min(len(knowledge.relations), 20) * 0.02

        # Source-grounded evidence is stronger than entity count. Keep the
        # contribution bounded so many repeated measurements cannot fabricate
        # confidence by volume alone.
        confidence += min(len(knowledge.facts), 10) * 0.02

        confidence = min(confidence, 1.0)

        return SearchContext(
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
            confidence=confidence,
            result_count=len(results),
        )
