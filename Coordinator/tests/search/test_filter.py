from core.search.filter import SearchFilter
from core.search.result import SearchResult

results = [

    SearchResult(
        title="Booking",
        url="https://booking.com",
        snippet="Tokyo hotels",
        authority=0.90,
    ),

    SearchResult(
        title="Random Blog",
        url="https://randomblog.xyz",
        snippet="Tokyo hotels",
        authority=0.50,
    ),

    SearchResult(
        title="Empty",
        url="https://example.com",
        snippet="",
        authority=0.95,
    ),

]

filtered = SearchFilter().filter(results)

print("\n===== FILTERED RESULTS =====\n")

for r in filtered:

    print(r.url)