"""
===========================================================
AIOS Long-Term Memory Manager
core/longterm/manager.py
===========================================================

Primary interface for Long-Term Memory.

Responsibilities

• Create memories
• Store memories
• Load memories
• Generate IDs

Coordinator should never access storage directly.

Version 1.0
===========================================================
"""

from uuid import uuid4

from core.longterm.models import (
    MemoryEntry,
    MemoryCategory,
    ImportanceLevel,
    current_timestamp,
)

from core.longterm.storage import LongTermStorage


class LongTermMemoryManager:

    def __init__(self):

        self.storage = LongTermStorage()

    # ==================================================
    # Create
    # ==================================================

    def create(

        self,

        title,

        summary,

        category=MemoryCategory.GENERAL,

        importance=ImportanceLevel.MEDIUM,

        keywords=None,

        source="USER",

    ):

        if keywords is None:

            keywords = []

        return MemoryEntry(

            id=self.generate_id(),

            timestamp=current_timestamp(),

            title=title,

            summary=summary,

            category=category,

            importance=importance,

            keywords=keywords,

            source=source,

        )

    # ==================================================
    # Save
    # ==================================================

    def save(

        self,

        memory,

    ):

        self.storage.append(memory)

    # ==================================================
    # Load
    # ==================================================

    def load_all(self):

        return self.storage.load()

    # ==================================================
    # ID Generator
    # ==================================================

    def generate_id(self):

        return f"mem_{uuid4().hex[:8]}"