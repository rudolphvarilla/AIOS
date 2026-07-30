"""
===========================================================
AIOS Semantic Registry
core/semantics/registry.py
===========================================================

Central semantic knowledge used BEFORE any LLM.

Purpose

• Detect user task
• Detect semantic domains
• Determine if search is required
• Determine if coding is required
• Determine if vision is required

This registry should remain lightweight and deterministic.

Version 1.0
===========================================================
"""

SEMANTIC_PATTERNS = {

    # --------------------------------------------------
    # Travel
    # --------------------------------------------------

    "hotel_search": {

        "keywords": [

            "hotel",
            "hotels",
            "stay",
            "stays",
            "accommodation",
            "hostel",
            "ryokan",
            "resort",

        ],

        "category": "travel",

        "task": "recommendation",

        "requires_search": True,

    },

    "flight_search": {

        "keywords": [

            "flight",
            "airfare",
            "ticket",
            "plane",

        ],

        "category": "travel",

        "task": "recommendation",

        "requires_search": True,

    },

    "restaurant_search": {

        "keywords": [

            "restaurant",
            "food",
            "eat",
            "cafe",
            "coffee",

        ],

        "category": "travel",

        "task": "recommendation",

        "requires_search": True,

    },

    # --------------------------------------------------
    # Coding
    # --------------------------------------------------

    "coding": {

        "keywords": [

            "python",
            "program",
            "script",
            "code",
            "function",
            "algorithm",

        ],

        "category": "coding",

        "task": "generation",

        "requires_code": True,

    },

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    "comparison": {

        "keywords": [

            "compare",
            "difference",
            "versus",
            "vs",

        ],

        "task": "comparison",

        "requires_search": True,

    },

    "review": {

        "keywords": [

            "review",
            "reviews",
            "opinion",
            "rating",

        ],

        "task": "research",

        "requires_search": True,

    },

    # --------------------------------------------------
    # Memory
    # --------------------------------------------------

    "memory": {

        "keywords": [

            "remember",
            "recall",
            "continue",
            "previous",
            "earlier",
            "history",

        ],

        "task": "memory",

    },

}