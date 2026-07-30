"""
===========================================================
AIOS Decision Rules
core/decision/rules.py
===========================================================

Semantic execution rules used by the Decision Engine.

The Context Engine determines WHAT the user is talking about.

Decision Rules determine WHAT AIOS should do next.

Version
2.0
===========================================================
"""

DOMAIN_RULES = {

    # ---------------------------------
    # Time
    # ---------------------------------

    "time": {

        "search": False,

        "background": False,

        "reason": "Semantic time query."

    },

    # ---------------------------------
    # Weather
    # ---------------------------------

    "weather": {

        "search": True,

        "background": False,

        "reason": "Weather requires live information."

    },

    # ---------------------------------
    # Coding
    # ---------------------------------

    "coding": {

        "search": False,

        "background": False,

        "reason": "Coding handled locally."

    },

    # ---------------------------------
    # Photography
    # ---------------------------------

    "photography": {

        "search": False,

        "background": False,

        "reason": "Photography knowledge available locally."

    },

    # ---------------------------------
    # Aviation
    # ---------------------------------

    "aviation": {

        "search": False,

        "background": False,

        "reason": "General aviation knowledge."

    },

    # ---------------------------------
    # Travel
    # ---------------------------------

    "travel": {

        "search": "conditional",

        "background": False,

        "reason": "Travel may require live information."

    },

    # ---------------------------------
    # Finance
    # ---------------------------------

    "finance": {

        "search": "conditional",

        "background": False,

        "reason": "Financial data may require live information."

    },

    # ---------------------------------
    # Business
    # ---------------------------------

    "business": {

        "search": False,

        "background": False,

        "reason": "General business knowledge."

    },

    # ---------------------------------
    # Legal
    # ---------------------------------

    "legal": {

        "search": "conditional",

        "background": False,

        "reason": "Legal information may require current laws."

    },

    # ---------------------------------
    # Filesystem
    # ---------------------------------

    "filesystem": {

        "search": False,

        "background": False,

        "reason": "Filesystem handled locally."

    },

    # ---------------------------------
    # Holidays
    # ---------------------------------

    "holidays": {

        "search": "conditional",

        "background": False,

        "reason": "Holiday dates may change by country."

    }

}