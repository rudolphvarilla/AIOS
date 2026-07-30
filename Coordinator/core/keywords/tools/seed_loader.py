"""
===========================================================
AIOS Seed Loader
core/keywords/tools/seed_loader.py
===========================================================

Loads every installed seed registry.

Seed registries are human-curated concept lists used by the
keyword generation pipeline.

Responsibilities

• Load seed modules
• Ignore missing modules
• Return successfully loaded modules

Version
1.0
===========================================================
"""

import importlib

from core.keywords.registry import KEYWORD_MODULES


class SeedLoader:

    def load(self):

        modules = []

        for module_name in KEYWORD_MODULES:

            try:

                module = importlib.import_module(
                    f"core.keywords.seeds.{module_name}"
                )

                modules.append(module)

            except Exception:

                continue

        return modules