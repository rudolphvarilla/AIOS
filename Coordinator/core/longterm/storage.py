"""
===========================================================
AIOS Long-Term Memory Storage
core/longterm/storage.py
===========================================================

Handles persistent storage of long-term memories.

Responsibilities

• Save memory entries
• Load memory entries
• Append entries
• Rewrite storage

No retrieval logic.
No scoring logic.

Version 1.0
===========================================================
"""

import json
from pathlib import Path

from core.longterm.models import (
    MemoryEntry,
    MemoryCategory,
    ImportanceLevel,
)


class LongTermStorage:

    def __init__(

        self,

        filepath="data/longterm_memory.json",

    ):

        self.filepath = Path(filepath)

        self.filepath.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

    # ==================================================

    def load(self):

        if not self.filepath.exists():

            return []

        with open(

            self.filepath,

            "r",

            encoding="utf-8",

        ) as file:

            raw = json.load(file)

        memories = []

        for item in raw:

            memories.append(

                MemoryEntry(

                    id=item["id"],

                    timestamp=item["timestamp"],

                    title=item["title"],

                    summary=item["summary"],

                    category=MemoryCategory(

                        item["category"]

                    ),

                    importance=ImportanceLevel(

                        item["importance"]

                    ),

                    keywords=item.get(

                        "keywords",

                        [],

                    ),

                    source=item.get(

                        "source",

                        "USER",

                    ),

                    last_accessed=item.get(

                        "last_accessed",

                        "",

                    ),

                    access_count=item.get(

                        "access_count",

                        0,

                    ),

                )

            )

        return memories

    # ==================================================

    def save(

        self,

        memories,

    ):

        raw = []

        for memory in memories:

            raw.append(

                {

                    "id": memory.id,

                    "timestamp": memory.timestamp,

                    "title": memory.title,

                    "summary": memory.summary,

                    "category": memory.category.value,

                    "importance": memory.importance.value,

                    "keywords": memory.keywords,

                    "source": memory.source,

                    "last_accessed": memory.last_accessed,

                    "access_count": memory.access_count,

                }

            )

        with open(

            self.filepath,

            "w",

            encoding="utf-8",

        ) as file:

            json.dump(

                raw,

                file,

                indent=4,

                ensure_ascii=False,

            )

    # ==================================================

    def append(

        self,

        memory,

    ):

        memories = self.load()

        memories.append(memory)

        self.save(memories)