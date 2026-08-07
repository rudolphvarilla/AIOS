from core.search.pipeline import SearchPipeline
from core.search.result import SearchResult

results = [
    SearchResult(
        title="Tokyo Hotels",
        url="https://booking.com",
        snippet="Booking.com provides thousands of hotels in Tokyo with reviews."
    ),
    SearchResult(
        title="Tokyo Hotels Duplicate",
        url="https://www.booking.com/",
        snippet="Duplicate"
    ),
    SearchResult(
        title="TripAdvisor",
        url="https://tripadvisor.com",
        snippet="Popular Tokyo hotels."
    )
]

pipeline = SearchPipeline()

unique, knowledge, context = pipeline.process(
    "best hotels in tokyo",
    results,
)

print("\n===== UNIQUE =====")
for item in unique:
    print(item.url)

print("\n===== SUMMARY =====")
print(context.summary)
