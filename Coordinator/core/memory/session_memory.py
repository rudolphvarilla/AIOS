"""
===========================================================
AIOS Session Memory
core/memory/session_memory.py

Stores complete conversation history for the current session.

Responsibilities

• Store every interaction
• Retrieve relevant interactions

Future

- Embedding search
- Vector retrieval
- Summarization
- Long-term transfer
===========================================================
"""

from dataclasses import dataclass, field


@dataclass
class SessionEntry:

    timestamp: str

    question: str

    answer: str

    model: str

    tool: str

    complexity: str


@dataclass
class SessionMemory:

    time: object = field(repr=False)

    history: list[SessionEntry] = field(default_factory=list)

    # =====================================================
    # Store
    # =====================================================

    def add(self, state):

        self.history.append(

            SessionEntry(

                timestamp=self.time.timestamp(),

                question=state.user_input,

                answer=state.response,

                model=state.selected_model,

                tool=str(state.selected_tool),

                complexity=state.plan.complexity,

            )

        )

    # =====================================================
    # Retrieve
    # =====================================================

    def retrieve(self, query: str, limit: int = 3):

        """
        Returns the most relevant SessionEntry objects.

        Current implementation:
            keyword overlap

        Future:
            embeddings
            vector search
        """

        if not self.history:

            return []

        tokens = {

            token.lower()

            for token in query.split()

        }

        scored = []

        for entry in self.history:

            score = 0

            question = entry.question.lower()

            answer = entry.answer.lower()

            for token in tokens:

                if token in question:

                    score += 2

                if token in answer:

                    score += 1

            if score > 0:

                scored.append((score, entry))

        if not scored:

            return []

        scored.sort(

            key=lambda item: item[0],

            reverse=True

        )

        return [

            entry

            for score, entry in scored[:limit]

        ]

    # =====================================================
    # Diagnostics
    # =====================================================

    def describe(self):

        return (

            f"Session Memory      : "

            f"{len(self.history)} entries"

        )