"""
===========================================================
AIOS Search Knowledge Enricher
core/search/enricher.py
===========================================================

Transforms extracted search knowledge into structured knowledge useful for
AI reasoning.

Phase 3.1.15 preserves deterministic fact records extracted directly from
search-result evidence while retaining relation-derived facts for backward
compatibility.
===========================================================
"""

from collections import defaultdict


class SearchKnowledgeEnricher:

    def enrich(self, knowledge):
        knowledge.recommendations = self.build_recommendations(knowledge.entities)
        knowledge.categories = self.build_categories(knowledge.entities)
        knowledge.locations = self.build_locations(knowledge.entities)
        knowledge.attributes = self.build_attributes(knowledge.entities)

        relation_facts = self.build_facts(
            knowledge.entities,
            knowledge.relations,
        )

        deterministic_facts = [
            fact.render() for fact in getattr(knowledge, "fact_records", [])
        ]

        knowledge.facts = deterministic_facts + relation_facts
        return knowledge

    def build_recommendations(self, entities):
        allowed = {"HOTEL", "RESTAURANT", "CAMERA", "PRODUCT", "BOOK"}
        recommendations = []
        seen = set()

        for entity in entities:
            if entity.entity_type not in allowed:
                continue
            if entity.name in seen:
                continue
            seen.add(entity.name)
            recommendations.append(entity.name)

        return recommendations

    def build_categories(self, entities):
        categories = defaultdict(list)
        for entity in entities:
            categories[entity.entity_type].append(entity.name)
        return dict(categories)

    def build_locations(self, entities):
        locations = []
        for entity in entities:
            if entity.entity_type in ("CITY", "COUNTRY", "DISTRICT", "AIRPORT"):
                locations.append(entity.name)
        return locations

    def build_attributes(self, entities):
        attributes = []
        for entity in entities:
            if entity.entity_type in ("ATTRIBUTE", "FEATURE"):
                attributes.append(entity.name)
        return attributes

    def build_facts(self, entities, relations):
        return [
            f"{relation.source} {relation.relation} {relation.target}"
            for relation in relations
        ]
