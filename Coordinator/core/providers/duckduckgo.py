"""
===========================================================
AIOS DuckDuckGo Provider
core/providers/duckduckgo.py
===========================================================

Implements the AIOS Provider interface.

Returns SearchResult objects.

Version 2
===========================================================
"""

from ddgs import DDGS

from core.providers.base import Provider
from core.search.result import SearchResult


class DuckDuckGoProvider(Provider):

    def execute(self, query, max_results=5):

        results = []

        with DDGS() as ddgs:

            response = list(

                ddgs.text(

                    query,

                    max_results=max_results,

                )

            )

        for item in response:

            results.append(

                SearchResult(

                    title=item.get("title", ""),

                    url=item.get("href", ""),

                    snippet=item.get("body", ""),

                    source="DuckDuckGo",

                )

            )

        return results