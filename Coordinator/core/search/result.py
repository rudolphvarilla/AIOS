"""
===========================================================
AIOS Search Result
core/search/result.py
===========================================================

Represents one processed search result.

Version 1.0
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