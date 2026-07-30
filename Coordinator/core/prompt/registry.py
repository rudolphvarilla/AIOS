"""
===========================================================
AIOS Prompt Registry
core/prompt/registry.py
===========================================================

Single source of truth for installed Prompt Blocks.

PromptBuilder never hardcodes Prompt Blocks.

PromptBlockLoader imports every registered block.

Future
------
• Plugin Prompt Blocks
• Third-party Prompt Blocks
• Dynamic Prompt Modules
• Auto-discovery

Version
1.0
===========================================================
"""

PROMPT_BLOCKS = {

    "repository":
        "core.prompt.blocks.repository_block.RepositoryBlock",

    "memory":
        "core.prompt.blocks.memory_block.MemoryBlock",

    "profile":
        "core.prompt.blocks.profile_block.ProfileBlock",

    "workspace":
        "core.prompt.blocks.workspace_block.WorkspaceBlock",

    "time":
        "core.prompt.blocks.time_block.TimeBlock",

    "user":
        "core.prompt.blocks.user_block.UserBlock",

    "search":
        "core.prompt.blocks.search_block.SearchBlock",

    "longterm":
        "core.prompt.blocks.longterm_block.LongTermBlock",

}