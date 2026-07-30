from core.services.search.service import SearchService

service = SearchService()

results = service.search(
    "Bernoulli principle",
    max_results=3
)

print()

print("=" * 50)
print("SEARCH RESULTS")
print("=" * 50)

for item in results:

    print(item)