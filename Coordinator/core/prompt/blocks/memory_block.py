"""
===========================================================
AIOS Memory Prompt Block
core/prompt/blocks/memory_block.py
===========================================================

Builds the memory portion of every AI prompt.

Responsibilities

• Working Memory
• Session Memory
• Memory Formatting
• Memory Filtering

This module converts memory objects into prompt text.

No retrieval logic exists here.

Used by

• PromptBuilder

Future

- Repository Memory
- Long-Term Memory
- Knowledge Graph
===========================================================
"""

class MemoryBlock:

    def enabled(self, state):

        if state.plan is None:

            return True

        return state.plan.memory

    def build(self, state):

        prompt = ""

        prompt += self.build_session_memory(state)

        return prompt

    # =========================================================

    def build_session_memory(self, state):

        if state.working_memory is None:

            return ""

        history = state.working_memory.session.history

        if len(history) == 0:

            return ""

        text = (
            "SESSION MEMORY\n"
            "--------------------\n"
        )

        results = state.working_memory.session.retrieve(
            state.user_input,
            limit=3
        )

        if not results:
            return ""

        for i, item in enumerate(results, start=1):

            text += (

                f"[{i}]\n"

                f"Question : {item.question}\n"

                f"Answer   : {item.answer}\n\n"

            )

        return text