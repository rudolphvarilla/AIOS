"""
===========================================================
AIOS Search Ranker
core/search/ranker.py
===========================================================

Ranks search results using authority score.

Version 1.0
===========================================================
"""

from core.search.authority import AuthorityScorer


class SearchRanker:

    def __init__(self):

        self.authority = AuthorityScorer()

    def rank(self, results):

        for result in results:

            result.authority = self.authority.score(result.url)

        results.sort(
            key=lambda r: r.authority,
            reverse=True,
        )

        return results