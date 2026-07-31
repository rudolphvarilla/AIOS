"""
AIOS Search Service
core/services/search_service.py

Provides Internet search capability.

The Executor never communicates directly
with Providers.

Instead, it delegates to the Search Service,
which selects the best available Provider.

Version 1
"""

from core.providers.manager import ProviderManager


class SearchService:

    def __init__(self):

        self.provider_manager = ProviderManager()

    # ----------------------------------
    # Internet Search
    # ----------------------------------

    def search(
        self,
        query,
        max_results=5
    ):

        provider = self.provider_manager.select(
            "SEARCH"
        )

        if provider is None:

            print()

            print("No SEARCH provider available.")

            return []

        return provider.execute(
            query=query,
            max_results=max_results
        )