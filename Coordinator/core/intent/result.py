"""
===========================================================
AIOS Intent Result
core/intent/result.py
===========================================================

Stores the result produced by the Intent Classifier.

Version 2.0
===========================================================
"""

from dataclasses import dataclass


@dataclass
class IntentResult:

    # -------------------------
    # Classification
    # -------------------------

    intent: str

    capability: str

    complexity: str = "LOW"

    # -------------------------
    # Metadata
    # -------------------------

    confidence: float = 1.0

    reasoning: str = ""