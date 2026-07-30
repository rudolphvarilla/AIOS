"""
===========================================================
AIOS Prompt Loader
core/prompt/loader.py
===========================================================

Loads every Prompt Block registered in registry.py.

PromptBuilder should never import individual blocks.

Future
------
- Plugin prompt blocks
- Dynamic loading
- External extensions

Version 1
===========================================================
"""

import importlib

from core.prompt.registry import PROMPT_BLOCKS


class PromptLoader:

    def load(self):

        blocks = {}

        for name, path in PROMPT_BLOCKS.items():

            try:

                module_name, class_name = path.rsplit(".", 1)

                module = importlib.import_module(module_name)

                cls = getattr(module, class_name)

                blocks[name] = cls()

            except Exception:

                continue

        return blocks