"""
AIOS Search Service
core/services/search_service.py

Provides Internet search capability.

The Executor never communicates directly
with Providers.

Instead, it delegates to the Search Service,
which aggregates results from all available
SEARCH providers.

Version 2
"""

from core.providers.manager import ProviderManager
from core.search.aggregator import SearchAggregator


class SearchService:

    def __init__(self):

        self.provider_manager = ProviderManager()
        self.aggregator = SearchAggregator(
            self.provider_manager
        )

    # ----------------------------------
    # Internet Search
    # ----------------------------------

    def search(
        self,
        query,
        max_results=5
    ):

        return self.aggregator.search(
            query=query,
            max_results=max_results,
        )
