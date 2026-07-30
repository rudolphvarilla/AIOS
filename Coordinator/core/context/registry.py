"""
===========================================================
AIOS Context Registry
core/context/registry.py
===========================================================

Description

Central registry of every keyword domain installed in AIOS.

The Context Engine queries this registry instead of hardcoding
knowledge modules.

Every keyword file registered here represents one semantic
domain.

Examples

travel.py
aviation.py
photography.py
finance.py

Responsibilities

• Register installed keyword domains

• Provide discovery for Context Engine

• Remain configuration-only

Future Expansion

Eventually this registry will automatically discover modules
using importlib and pathlib instead of maintaining a manual list.

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

    "time",

]