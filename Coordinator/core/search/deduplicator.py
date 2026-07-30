"""
===========================================================
AIOS Search Deduplicator
core/search/deduplicator.py
===========================================================

Removes duplicate search results.

Version 1.0
===========================================================
"""

from urllib.parse import urlparse

from core.search.result import SearchResult


class SearchDeduplicator:

    def deduplicate(
        self,
        results: list[SearchResult],
    ) -> list[SearchResult]:

        seen = set()
        unique = []

        for result in results:

            key = self._canonical(result.url)

            if key in seen:
                continue

            seen.add(key)
            unique.append(result)

        return unique

    # -----------------------------------------------------

    def _canonical(self, url: str) -> str:

        parsed = urlparse(url)

        host = parsed.netloc.lower()

        if host.startswith("www."):
            host = host[4:]

        path = parsed.path.rstrip("/").lower()

        return f"{host}{path}"