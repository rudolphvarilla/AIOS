"""
===========================================================
AIOS Search Summarizer
core/search/summarizer.py

Produces a lightweight textual summary of search results.

Version 4
===========================================================
"""


class SearchSummarizer:

    def summarize(
        self,
        query,
        results,
    ):

        return self.build_summary(

            query,

            results,

        )

    # -------------------------------------------------

    def build_summary(
        self,
        query,
        results,
    ):

        if not results:

            return "No relevant search results were found."

        snippets = []

        for result in results[:3]:

            text = getattr(result, "summary", None)

            if not text:

                text = result.snippet

            if text:

                snippets.append(

                    " ".join(text.split())

                )

        return " ".join(snippets)