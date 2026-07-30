from core.providers.duckduckgo import DuckDuckGoProvider

provider = DuckDuckGoProvider()

results = provider.execute(
    "Bernoulli Principle",
    max_results=3
)

print()

print("=" * 60)
print("RESULTS")
print("=" * 60)

for i, result in enumerate(results, start=1):

    print()

    print(f"[{i}]")

    print("Title:")
    print(result["title"])

    print()

    print("URL:")
    print(result["url"])

    print()

    print("Snippet:")
    print(result["snippet"])