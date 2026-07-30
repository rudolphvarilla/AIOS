"""
===========================================================
AIOS Semantic Detector
core/semantics/detector.py
===========================================================

Detects semantic patterns from raw user input.

This module performs lightweight semantic detection before
any LLM is called.

Responsibilities

• Detect semantic categories
• Detect semantic tasks
• Detect execution hints
• Return matching semantic patterns

Version 1.0
===========================================================
"""

from core.semantics.registry import SEMANTIC_PATTERNS


class SemanticDetector:

    def detect(self, text: str):

        text = text.casefold()

        matches = []

        for name, pattern in SEMANTIC_PATTERNS.items():

            keywords = pattern.get("keywords", [])

            if any(keyword in text for keyword in keywords):

                matches.append({

                    "name": name,

                    **pattern

                })

        print("\n===== SEMANTIC DETECTOR =====")

        for match in matches:

            print(match["name"])

        return matches