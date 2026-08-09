"""
===========================================================
AIOS Time Keyword Registry
core/keywords/registries/time.py
===========================================================

Semantic Registry v3

Canonical concepts for temporal reasoning.

Important distinction
---------------------
"current" is not automatically "current time". It can mean the present
state/latest observation in another domain. The Context Engine resolves this
ambiguity using semantic intent.

Version 3
===========================================================
"""

TIME = {
    "today": {
        "keywords": {"today"},
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
    "tomorrow": {
        "keywords": {"tomorrow"},
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
    "yesterday": {
        "keywords": {"yesterday"},
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
    "current_time": {
        "keywords": {
            "time", "time now", "current time", "clock", "what time",
        },
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
    "present_state": {
        "keywords": {
            "current", "currently", "now", "present", "latest", "recent",
            "recently", "up to date", "up-to-date", "as of now",
        },
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": {"temporal_scope"},
    },
    "current_date": {
        "keywords": {
            "date", "today's date", "current date", "calendar",
        },
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
    "weekday": {
        "keywords": {
            "weekday", "monday", "tuesday", "wednesday", "thursday",
            "friday", "saturday", "sunday",
        },
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
    "relative_time": {
        "keywords": {
            "next week", "last week", "next month", "last month",
            "next year", "last year", "this week", "this month", "this year",
        },
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
    "duration": {
        "keywords": {
            "hour", "hours", "minute", "minutes", "second", "seconds",
            "day", "days", "week", "weeks", "month", "months", "year", "years",
        },
        "confidence": 1.0,
        "last_updated": None,
        "source": "manual",
        "relationships": set(),
    },
}
