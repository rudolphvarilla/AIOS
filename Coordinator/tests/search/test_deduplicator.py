from core.search.deduplicator import SearchDeduplicator
from core.search.result import SearchResult

results = [

    SearchResult(
        title="A",
        url="https://booking.com",
        snippet=""
    ),

    SearchResult(
        title="B",
        url="https://www.booking.com/",
        snippet=""
    ),

    SearchResult(
        title="C",
        url="https://tripadvisor.com",
        snippet=""
    ),

    SearchResult(
        title="D",
        url="https://booking.com/",
        snippet=""
    ),

]

dedup = SearchDeduplicator()

unique = dedup.deduplicate(results)

print("\n===== UNIQUE RESULTS =====\n")

for item in unique:
    print(item.url)