"""
Defines the priority of every AIOS context source.
/core/prompt/context_priority.py

Higher priority context overrides lower priority context.
"""

CONTEXT_PRIORITY = [

    "repository",
    "profile",
    "workspace",
    "memory",
    "time",
    "search",
    "user"

]