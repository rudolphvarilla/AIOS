"""
===========================================================
AIOS Search Relevance
core/search/relevance.py
===========================================================

Calculates how relevant a search result is to the query.

Version 1.0
===========================================================
"""

import re


class RelevanceScorer:

    def score(self, query, title, snippet):

        query_words = self._tokenize(query)

        text = self._tokenize(title + " " + snippet)

        if not query_words:
            return 0.0

        matches = sum(

            1

            for word in query_words

            if word in text

        )

        return matches / len(query_words)

    def _tokenize(self, text):

        return set(

            re.findall(

                r"[a-z0-9]+",

                text.lower(),

            )

        )