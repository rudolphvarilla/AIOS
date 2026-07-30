"""
===========================================================
AIOS Long-Term Memory Prompt Block
core/prompt/blocks/longterm_block.py
===========================================================

Builds the Long-Term Memory section of the prompt.

Only formats retrieved memories.

Retrieval is performed before PromptBuilder.

Version 1.0
===========================================================
"""


class LongTermBlock:

    def enabled(self, state):

        return bool(state.longterm_memories)

    # ==================================================

    def build(self, state):

        if not state.longterm_memories:

            return ""

        lines = []

        lines.append("LONG-TERM MEMORY")
        lines.append("--------------------")
        lines.append("")

        for memory in state.longterm_memories:

            lines.append(f"• {memory.title}")

            lines.append(f"  {memory.summary}")

            lines.append("")

        return "\n".join(lines)