"""
===========================================================
AIOS Search Filter
core/search/filter.py
===========================================================

Filters search results before ranking.
===========================================================
"""

from core.config import MIN_SEARCH_AUTHORITY


class SearchFilter:

    def filter(self, query_or_results, results=None):
        """Filter results while supporting both legacy and pipeline call forms.

        Legacy callers may use ``filter(results)``. The pipeline may use
        ``filter(query, results)`` when query-aware filtering is available.
        Query is currently informational and does not alter deterministic
        authority/required-field filtering.
        """
        if results is None:
            results = query_or_results

        filtered = []

        # Debug once per call, not once per result.
        print("\n===== FILTER DEBUG =====")
        for debug_result in results or []:
            print(f"{debug_result.authority:.2f} | {debug_result.title}")

        for result in results or []:
            if not result.title:
                continue
            if not result.url:
                continue
            if not result.snippet:
                continue
            if result.authority < MIN_SEARCH_AUTHORITY:
                continue
            filtered.append(result)

        return filtered