"""
===========================================================
AIOS Intent Classifier
core/intent/classifier.py
===========================================================

Intent classification based on semantic context.

The classifier no longer owns keyword lists.

All semantic knowledge comes from the Context Engine.

Version 2.0
===========================================================
"""

from core.intent.result import IntentResult


class IntentClassifier:

    # -----------------------------------------
    # Domain → Capability Mapping
    # -----------------------------------------

    DOMAIN_CAPABILITY = {

        "coding": ("CODING", "CODING"),

        "filesystem": ("CODING", "CODING"),

        "travel": ("GENERAL", "GENERAL"),

        "photography": ("GENERAL", "GENERAL"),

        "videography": ("GENERAL", "GENERAL"),

        "aviation": ("GENERAL", "GENERAL"),

        "engineering": ("GENERAL", "GENERAL"),

        "finance": ("GENERAL", "GENERAL"),

        "business": ("GENERAL", "GENERAL"),

        "legal": ("GENERAL", "GENERAL"),

        "time": ("GENERAL", "GENERAL"),

    }

    # -----------------------------------------

    def classify(self, context):

        # No semantic domains detected

        if not context.domains:

            return IntentResult(

                intent="GENERAL",

                complexity="LOW",

                capability="GENERAL",

                confidence=1.0,

                reasoning="No semantic domains detected."

            )

        primary = context.primary_domain

        intent, capability = self.DOMAIN_CAPABILITY.get(

            primary,

            ("GENERAL", "GENERAL")

        )

        return IntentResult(

            intent=intent,

            capability=capability,

            confidence=context.domain_scores.get(primary, 1.0),

            reasoning=f"Primary semantic domain '{primary}'."

        )