"""
===========================================================
AIOS Runtime Configuration
core/config.py
===========================================================

Central runtime configuration for AIOS.

Stores system-wide default settings used throughout the
Coordinator unless explicitly overridden.

Current Settings

• Default Personality
• Default Model
• Default Search Provider
• Simulation Mode

Future Settings

• Logging
• Feature Flags
• Plugin Configuration
• Provider Priorities
===========================================================
"""

# -------------------------------------------------
# Runtime Defaults
# -------------------------------------------------

DEFAULT_PERSONALITY = "default"

DEFAULT_MODEL = None

DEFAULT_SEARCH_PROVIDER = None

SIMULATION_MODE = False


# -------------------------------------------------
# Prompt Builder
# -------------------------------------------------

PROMPT_PREVIEW_LIMIT = 1200


# -------------------------------------------------
# Background Jobs
# -------------------------------------------------

DEFAULT_BACKGROUND_SUMMARY = "Summarize previous response"


# -------------------------------------------------
# Performance
# -------------------------------------------------

TOKEN_ESTIMATE_DIVISOR = 4

# ----------------------------------------
# Search
# ----------------------------------------

MIN_SEARCH_AUTHORITY = 0.50

# ----------------------------------------
# Decision Confidence
# ----------------------------------------

DECISION_CONFIDENCE_THRESHOLD = 0.80