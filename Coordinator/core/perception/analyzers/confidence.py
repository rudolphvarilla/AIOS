"""
===========================================================
AIOS Confidence Analyzer
core/perception/analyzers/confidence.py
===========================================================

Produces an overall perception confidence.

This is NOT routing confidence.

It measures how much structured information was extracted.
===========================================================
"""


class ConfidenceAnalyzer:

    def compute(self, result):

        score = 0.0

        if result.entities:
            score += 1.0

        if result.requirements:
            score += 1.0

        if result.repository_targets:
            score += 1.0

        return score / 3.0