"""
AIOS Search Result Aggregator
core/search/aggregator.py

Combines results from multiple search providers into one
provider-neutral result set.

Responsibilities

• execute enabled search providers
• tolerate individual provider failures
• preserve provider identity
• deduplicate equivalent URLs
• enforce a global result limit

Version 1.0
"""


class SearchAggregator:

    def __init__(self, provider_manager):
        self.provider_manager = provider_manager

    # -----------------------------------------------------
    # Aggregate search results
    # -----------------------------------------------------

    def search(
        self,
        query,
        max_results=5,
    ):
        """Search all available SEARCH providers and merge their results."""

        providers = self.provider_manager.select_all("SEARCH")

        if not providers:
            return []

        combined = []
        seen_urls = set()

        for provider in providers:
            try:
                results = provider.execute(
                    query=query,
                    max_results=max_results,
                ) or []
            except Exception as exc:
                print(
                    f"[SEARCH] Provider failed: {provider.__class__.__name__}: {exc}"
                )
                continue

            for result in results:
                url = (result.url or "").strip()

                # A result without a URL cannot be safely deduplicated.
                # Keep it, but do not let repeated empty URLs collapse.
                if url and url in seen_urls:
                    continue

                if url:
                    seen_urls.add(url)

                combined.append(result)

        return combined[:max_results]
