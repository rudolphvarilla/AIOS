"""
===========================================================
AIOS Keyword Manager
core/keywords/manager.py
===========================================================

Description

Central manager for every semantic registry.

All registry modifications must go through this class.

Responsibilities
----------------
• Load registries
• Retrieve registries
• Add concepts
• Add keywords
• Prevent duplicates

Future
------
• Registry persistence
• Confidence updates
• Relationship updates
• Automatic merges
• Version history
• Semantic Evolution integration

Version
1.0
===========================================================
"""

from core.keywords.registry import KEYWORD_MODULES
from core.keywords.registry_writer import RegistryWriter
from core.keywords.registry_validator import RegistryValidator
import importlib
import sys


class KeywordManager:

    def __init__(self):

        self.registries = {}

        self.writer = RegistryWriter()

        self.validator = RegistryValidator()

        self.load(verbose=True)

    # --------------------------------------------------
    # Load registries
    # --------------------------------------------------

    def load(self, verbose=True):

        self.registries.clear()

        for module_name in KEYWORD_MODULES:

            try:

                module = importlib.import_module(
                    f"core.keywords.registries.{module_name}"
                )

                registry_name = module_name.upper()

                if not hasattr(module, registry_name):

                    if verbose:

                        print(
                            f"[KeywordManager] {module_name} not upgraded yet."
                        )

                    continue

                registry = getattr(module, registry_name)

                self.registries[module_name] = registry

            except Exception as e:

                if verbose:

                    print(
                        f"[KeywordManager] Failed loading {module_name}: {e}"
                    )

    # --------------------------------------------------
    # Get registry
    # --------------------------------------------------

    def get(self, domain):

        return self.registries.get(domain)

    # --------------------------------------------------
    # Add concept
    # --------------------------------------------------

    def add_concept(self, domain, concept):

        registry = self.get(domain)

        if registry is None:

            return False

        if concept in registry:

            return False

        registry[concept] = {

            "keywords": set(),

            "confidence": 1.0,

            "last_updated": None,

            "source": "manual",

            "relationships": set(),

        }

        return True

    # --------------------------------------------------
    # Add keyword
    # --------------------------------------------------

    def add_keyword(self, domain, concept, keyword):

        registry = self.get(domain)

        if registry is None:

            return False

        if concept not in registry:

            self.add_concept(domain, concept)

        registry[concept]["keywords"].add(

            keyword.lower()

        )

        return True

    # --------------------------------------------------
    # Registry list
    # --------------------------------------------------

    def domains(self):

        return list(self.registries.keys())

    # --------------------------------------------------
    # Concepts
    # --------------------------------------------------

    def concepts(self, domain):

        registry = self.get(domain)

        if registry is None:

            return []

        return list(registry.keys())

    # --------------------------------------------------
    # Save registry
    # --------------------------------------------------

    def save(self, domain):

        registry = self.get(domain)

        if registry is None:

            return False, "Unknown registry."

        self.writer.save(domain, registry, generated=True)

        ok, reason = self.validator.validate(domain)

        if not ok:

            return False, reason

        module_name = f"core.keywords.registries.{domain}"

        if module_name in sys.modules:

            importlib.reload(sys.modules[module_name])

        self.load(verbose=False)

        return True, "Registry saved."

