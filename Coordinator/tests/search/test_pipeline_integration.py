"""
Regression Test 56.4
Search Pipeline Integration
"""

from core.search.pipeline import SearchPipeline
from core.search.result import SearchResult

pipeline = SearchPipeline()

results = [

    SearchResult(
        title="Aman Tokyo",
        url="https://www.aman.com/resorts/aman-tokyo",
        snippet="Luxury hotel in Tokyo, Japan.",
        authority=98,
        source="Tripadvisor",
    ),

    SearchResult(
        title="Tokyo Hotels",
        url="https://booking.com",
        snippet="Hotels in Tokyo with reviews.",
        authority=95,
        source="Booking",
    ),

]

unique, knowledge, context = pipeline.process(

    query="best hotels in tokyo",

    results=results,

)

print("\n===== UNIQUE RESULTS =====")

for r in unique:

    print(f"{r.title}")

print("\n===== ENTITIES =====")

for entity in knowledge.entities:

    print(

        f"{entity.name} -> {entity.entity_type}"

    )

print("\n===== RELATIONS =====")

for relation in knowledge.relations:

    print(

        f"{relation.source} {relation.relationship} {relation.target}"

    )

print("\n===== SEARCH CONTEXT =====")

print(f"Topic      : {context.topic}")

print(f"Confidence : {context.confidence}")

print(f"Sources    : {context.source_count}")

print("\nRecommendations")

for recommendation in context.recommendations:

    print(recommendation)

print("\n===== SUMMARY =====")

print(context.summary)