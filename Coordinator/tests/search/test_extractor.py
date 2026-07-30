from core.search.extractor import SearchExtractor
from core.search.result import SearchResult

results = [

    SearchResult(

        title="THE 10 BEST Hotels in Tokyo",

        url="https://tripadvisor.com",

        snippet="Aman Tokyo Park Hyatt Tokyo Imperial Hotel"

    )

]

knowledge = SearchExtractor().extract(

    results

)

print()

print("===== ENTITIES =====")

print()

for entity in knowledge.entities:

    print(

        entity.name,

        entity.entity_type,

    )