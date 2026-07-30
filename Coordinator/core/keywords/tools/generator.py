"""
===========================================================
AIOS Keyword Generator
core/keywords/tools/generator.py
===========================================================

Generates candidate keywords from seed registries.

Version 1 performs no AI generation.

Instead it simply collects every seed keyword and returns
them as candidate keywords.

Future versions

• LLM expansion
• Synonym generation
• Hypernym expansion
• Geographic expansion
• Industry-specific expansion
• Multi-language expansion
===========================================================
"""

from core.keywords.tools.seed_loader import SeedLoader


class KeywordGenerator:

    def __init__(self):

        self.loader = SeedLoader()

    def generate(self):

        modules = self.loader.load()

        generated = {}

        for module in modules:

            if hasattr(module, "SEED_KEYWORDS"):

                generated[module.__name__] = list(module.SEED_KEYWORDS)

        return generated