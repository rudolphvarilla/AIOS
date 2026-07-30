"""
===========================================================
AIOS Keyword Registry
core/keywords/registry.py
===========================================================

Description

Registers every keyword module available to AIOS.

The registry serves as the single source of truth for semantic
domains recognized by the Context Engine.

Responsibilities:
• Maintain installed keyword modules
• Provide discovery to the Loader
• Never perform matching
• Never analyze text

Future

Later versions will automatically discover modules using
pathlib instead of maintaining this list manually.

Version
1.0
===========================================================
"""

KEYWORD_MODULES = [

    "travel",
    "photography",
    "videography",
    "aviation",
    "engineering",
    "finance",
    "business",
    "legal",
    "coding",
    "filesystem",
    "time",

]
