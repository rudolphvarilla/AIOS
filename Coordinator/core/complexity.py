"""
AIOS Complexity Analyzer

Determines how much reasoning a prompt requires.

Output:
    LOW
    MEDIUM
    HIGH

Future versions may replace these rules with an LLM-based analyzer.
"""

import re

COMPLEXITY_ORDER = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
}

HIGH_KEYWORDS = [
    "derive",
    "derivation",
    "prove",
    "proof",
    "analyze",
    "analysis",
    "design",
    "optimize",
    "optimization",
    "justify",
    "evaluate",
    "research",
    "step by step",
    "in detail",
    "compare",
    "contrast",
    "critique",
    "formulate",
    "synthesize",
]

MEDIUM_KEYWORDS = [
    "calculate",
    "solve",
    "how does",
    "why does",
    "difference",
    "advantages",
    "disadvantages",
    "explain",
    "draft",
]


def classify_complexity(prompt: str) -> str:

    text = prompt.lower()

    # HIGH complexity keywords
    for keyword in HIGH_KEYWORDS:
        if keyword in text:
            return "HIGH"

    # MEDIUM complexity keywords
    for keyword in MEDIUM_KEYWORDS:
        if keyword in text:
            return "MEDIUM"

    # Long prompts generally require more reasoning
    words = re.findall(r"\w+", text)

    if len(words) > 75:
        return "MEDIUM"

    return "LOW"