"""
===========================================================
AIOS Search Filter
core/search/filter.py
===========================================================

Filters search results before ranking.

Responsibilities

• Remove incomplete results
• Remove low-authority sources
• Remove empty snippets
• Future:
    - NSFW filtering
    - Language filtering
    - Duplicate domain filtering

Version 1.0
===========================================================
"""

from core.config import MIN_SEARCH_AUTHORITY


class SearchFilter:

    def filter(self, query, results):

        filtered = []

        for result in results:

            # -----------------------------
            # Required fields
            # -----------------------------

            if not result.title:
                continue

            if not result.url:
                continue

            if not result.snippet:
                continue

            # -----------------------------
            # Debug Mode - Show ranking of filtered
            # -----------------------------

            print("\n===== FILTER DEBUG =====")

            for debug_result in results:
                print(
                    f"{debug_result.authority:.2f} | {debug_result.title}"
                )

            # -----------------------------
            # Authority threshold
            # -----------------------------

            if result.authority < MIN_SEARCH_AUTHORITY:
                continue

            filtered.append(result)

        return filtered