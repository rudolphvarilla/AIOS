"""
===========================================================
AIOS Search Result
core/search/result.py
===========================================================

Represents one processed search result.

Version 1.1
===========================================================
"""

from dataclasses import dataclass


@dataclass
class SearchResult:

    title: str
    url: str
    snippet: str

    authority: float = 0.50
    rank: int = 0
    source: str = ""

    def __getitem__(self, key):
        """Provide read-only mapping compatibility for legacy callers."""
        if key in {"title", "url", "snippet", "authority", "rank", "source"}:
            return getattr(self, key)
        raise KeyError(key)
