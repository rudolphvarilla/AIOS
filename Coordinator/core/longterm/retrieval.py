"""
===========================================================
AIOS Long-Term Memory Retrieval
core/longterm/retrieval.py
===========================================================

Retrieves relevant memories.

Strategy

• Keyword matching
• Importance bonus
• Recency placeholder

Version 1.0
===========================================================
"""

from core.longterm.storage import LongTermStorage


class LongTermRetrieval:

    def __init__(self):

        self.storage = LongTermStorage()

    # ==================================================

    def retrieve(

        self,

        query,

        limit=5,

    ):

        memories = self.storage.load()

        words = {

            word.lower()

            for word in query.split()

        }

        scored = []

        for memory in memories:

            score = self.score(

                memory,

                words,

            )

            if score > 0:

                scored.append(

                    (

                        score,

                        memory,

                    )

                )

        scored.sort(

            key=lambda x: x[0],

            reverse=True,

        )

        return [

            memory

            for _, memory in scored[:limit]

        ]

    # ==================================================

    def score(self, memory,words,):

        match_score = 0

        # -----------------------------
        # Title
        # -----------------------------

        title = memory.title.lower()

        for word in words:

            if word in title:

                match_score += 10

        # -----------------------------
        # Summary
        # -----------------------------

        summary = memory.summary.lower()

        for word in words:

            if word in summary:

                match_score += 5

        # -----------------------------
        # Keywords
        # -----------------------------

        keywords = {

            keyword.lower()

            for keyword in memory.keywords

        }

        match_score += len(words & keywords) * 20

        # -----------------------------
        # No textual match
        # -----------------------------

        if match_score ==0:
            return 0

        score = match_score

        # -----------------------------
        # Importance bonus
        # -----------------------------

        match memory.importance.value:

            case "LOW":
                score += 1
            case "MEDIUM":
                score += 3
            case "HIGH":
                score += 6
            case "CRITICAL":
                score += 10

        return score