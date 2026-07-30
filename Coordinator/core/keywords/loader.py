"""
===========================================================
AIOS Keyword Loader
core/keywords/loader.py
===========================================================

Description
Loads every installed keyword module.

The Context Engine does not know where keyword files are.

The Loader handles importing every registered module.

Responsibilities
• Load keyword modules
• Skip invalid modules safely
• Return loaded modules

Future
- Automatic discovery
- Plugin support
- Third-party registries
- Hot reload

Version
1.0
===========================================================
"""

import importlib

from core.keywords.registry import KEYWORD_MODULES


class KeywordLoader:

    def load(self):

        modules = []

        for module_name in KEYWORD_MODULES:

            try:

                module = importlib.import_module(
                    f"core.keywords.registries.{module_name}"
                )

                modules.append(module)

            except Exception as e:

                print(f"[KeywordLoader] Failed to load {module_name}: {e}")

        return modules