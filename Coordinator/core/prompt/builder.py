"""
===========================================================
AIOS Prompt Builder
core/prompt/builder.py
===========================================================

Constructs the final prompt sent to the selected language model.

Version 5

Architecture

Permanent Prompt
----------------
• SystemPrompt
• PersonalityPrompt

Dynamic Prompt Blocks
---------------------
• RepositoryBlock
• MemoryBlock
• ProfileBlock
• WorkspaceBlock
• TimeBlock
• UserBlock
• SearchBlock
• LongTermMemoryBlock

Prompt Builder no longer contains prompt logic.

Each block is responsible for building itself.

Empty blocks are automatically skipped.
"""

from core.prompt.loader import PromptLoader
from core.prompt.planner import PromptPlanner
from core.prompt.system import SystemPrompt
from core.prompt.personality import PersonalityPrompt
from core.prompt.context_priority import CONTEXT_PRIORITY

class PromptBuilder:

    def __init__(self):
        self.planner = PromptPlanner()
        self.system_prompt = SystemPrompt()
        self.personality = PersonalityPrompt()
        self.loader = PromptLoader()
        self.blocks = self.loader.load()

    def build(self, state):

        plan = self.planner.plan(state)

        state.prompt_plan = plan

        sections = []

        # ----------------------------------------
        # Permanent AIOS Identity
        # ----------------------------------------

        system = self.system_prompt.build()

        if system:
            sections.append(system)

        personality = self.personality.build()

        if personality:
            sections.append(personality)

        for category in CONTEXT_PRIORITY:

            if not plan.get(category, False):

                continue

            block = self.blocks.get(category)

            if block is None:

                continue

            result = block.build(state)

            if result:

                sections.append(result)

        return "\n".join(sections)