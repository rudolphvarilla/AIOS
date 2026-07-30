"""
===========================================================
AIOS Search Authority
core/search/authority.py
===========================================================

Assigns trust scores to search sources.

Version 1.0
===========================================================
"""

from urllib.parse import urlparse


class AuthorityScorer:

    def __init__(self):

        self.rules = {

            # Official

            ".gov": 1.00,
            ".edu": 0.98,

            # Encyclopedic

            "wikipedia.org": 0.95,

            # Major documentation

            "python.org": 0.95,
            "developer.mozilla.org": 0.95,
            "docs.microsoft.com": 0.95,

            # Travel

            "booking.com": 0.90,
            "tripadvisor.com": 0.90,
            "agoda.com": 0.90,

            # News

            "reuters.com": 0.90,
            "bbc.com": 0.90,

            # Forums

            "reddit.com": 0.70,
            "quora.com": 0.65,

        }

    def score(self, url):

        host = urlparse(url).netloc.lower()

        if host.endswith(".gov"):
            return 1.0

        if host.endswith(".edu"):
            return 0.98

        for domain, score in self.rules.items():

            if domain in host:

                return score

        return 0.50

    # ==================================================
    # Apply authority scores to search results
    # ==================================================

    def apply(self, results):

        for result in results:

            result.authority = self.score(result.url)

        return results