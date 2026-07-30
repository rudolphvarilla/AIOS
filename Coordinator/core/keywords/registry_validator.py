"""
===========================================================
AIOS Registry Validator
core/keywords/registry_validator.py
===========================================================

Validates semantic registry files before they become
production registries.

Version 2.0

Data-only registry architecture.

Responsibilities
----------------
• Load registry module
• Verify registry variable exists
• Verify registry schema
• Verify required fields
• Verify keyword types
• Verify metadata

Future
------
• Duplicate keyword detection
• Cross-registry conflict detection
• Relationship validation
• Semantic consistency checks
===========================================================
"""

from pathlib import Path
import importlib.util


REQUIRED_FIELDS = {
    "keywords",
    "confidence",
    "last_updated",
    "source",
    "relationships",
}


class RegistryValidator:

    def validate(self, domain: str):

        registry_file = (
            Path("core/keywords/generated")
            / f"{domain}.py"
        )

        if not registry_file.exists():
            return False, "Generated registry not found."

        try:

            spec = importlib.util.spec_from_file_location(
                f"generated_{domain}",
                registry_file,
            )

            if spec is None or spec.loader is None:
                return False, "Unable to create module spec."

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        except Exception as e:
            return False, str(e)

        registry_name = domain.upper()

        if not hasattr(module, registry_name):
            return False, f"{registry_name} not found."

        registry = getattr(module, registry_name)

        if not isinstance(registry, dict):
            return False, "Registry is not a dictionary."

        for concept, data in registry.items():

            if not isinstance(data, dict):
                return False, f"{concept} is not a dictionary."

            missing = REQUIRED_FIELDS - set(data.keys())

            if missing:
                return False, (
                    f"{concept} missing {sorted(missing)}"
                )

            # -----------------------------
            # keywords
            # -----------------------------

            if not isinstance(data["keywords"], set):
                return False, (
                    f"{concept}.keywords must be a set."
                )

            if not all(
                isinstance(k, str)
                for k in data["keywords"]
            ):
                return False, (
                    f"{concept}.keywords contains non-string values."
                )

            # -----------------------------
            # confidence
            # -----------------------------

            if not isinstance(
                data["confidence"],
                (int, float),
            ):
                return False, (
                    f"{concept}.confidence must be numeric."
                )

            # -----------------------------
            # relationships
            # -----------------------------

            if not isinstance(
                data["relationships"],
                set,
            ):
                return False, (
                    f"{concept}.relationships must be a set."
                )

        return True, "Registry valid."