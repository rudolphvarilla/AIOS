"""
===========================================================
AIOS Repository Detector
core/perception/analyzers/repository_detector.py
===========================================================

Determines which repository modules are relevant to the
current request.

This does NOT retrieve information.

It only identifies potential repository targets.
===========================================================
"""

from dataclasses import dataclass


@dataclass
class RepositoryTarget:

    module: str

    confidence: float = 1.0


class RepositoryDetector:

    TARGETS = {

        "memory": {

            "remember",
            "favorite",
            "preference",
            "history",

        },

        "knowledge": {

            "what",
            "how",
            "why",
            "explain",

        },

        "events": {

            "schedule",
            "appointment",
            "meeting",
            "trip",
            "flight",

        },

        "relationships": {

            "friend",
            "family",
            "coworker",
            "contact",

        },

        "watchers": {

            "monitor",
            "watch",
            "track",
            "alert",

        }

    }

    def detect(self, text):

        text = text.lower()

        found = []

        for module, keywords in self.TARGETS.items():

            for keyword in keywords:

                if keyword in text:

                    found.append(

                        RepositoryTarget(

                            module,

                            1.0

                        )

                    )

                    break

        return found