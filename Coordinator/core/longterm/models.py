"""
===========================================================
AIOS Long-Term Memory Models
core/longterm/models.py
===========================================================

Defines all data models used by Long-Term Memory.

Contains

• Importance Levels
• Memory Categories
• MemoryEntry

No storage logic.
No retrieval logic.

Version 1.0
===========================================================
"""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


# ===========================================================
# Importance
# ===========================================================

class ImportanceLevel(Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


# ===========================================================
# Categories
# ===========================================================

class MemoryCategory(Enum):

    PERSONAL = "PERSONAL"

    TRAVEL = "TRAVEL"

    PHOTOGRAPHY = "PHOTOGRAPHY"

    ENGINEERING = "ENGINEERING"

    PROGRAMMING = "PROGRAMMING"

    PROJECT = "PROJECT"

    PREFERENCE = "PREFERENCE"

    GENERAL = "GENERAL"


# ===========================================================
# Memory Entry
# ===========================================================

@dataclass
class MemoryEntry:

    id: str

    timestamp: str

    title: str

    summary: str

    category: MemoryCategory

    importance: ImportanceLevel

    keywords: list[str] = field(default_factory=list)

    source: str = "USER"

    last_accessed: str = ""

    access_count: int = 0


# ===========================================================
# Helper
# ===========================================================

def current_timestamp():

    return datetime.now().isoformat()