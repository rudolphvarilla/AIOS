"""
===========================================================
AIOS Requirement Detector
core/perception/analyzers/requirement_detector.py
===========================================================

Extracts high-level user requirements.

Requirements describe WHAT the user wants.

Not:
- domain
- intent
- routing

Examples

"best hotels in tokyo"
    recommendation

"compare synology and ugreen"
    comparison

"explain lift equation"
    explanation

"remember favorite color"
    memory_update

===========================================================
"""

from dataclasses import dataclass


@dataclass
class Requirement:

    name: str

    confidence: float = 1.0


class RequirementDetector:

    REQUIREMENTS = {

        "recommendation": {

            "best",
            "recommend",
            "top",
            "good",

        },

        "comparison": {

            "compare",
            "difference",
            "versus",
            "vs",

        },

        "explanation": {

            "explain",
            "what is",
            "why",
            "how",

        },

        "creation": {

            "create",
            "design",
            "generate",
            "build",
            "write",

        },

        "memory_update": {

            "remember",
            "my favorite",
            "my name is",

        },

        "calculation": {

            "calculate",
            "solve",
            "compute",

        },

        "action": {

            "book",
            "reserve",
            "schedule",

        }

    }

    def detect(self, text):

        text = text.lower()

        found = []

        for requirement, keywords in self.REQUIREMENTS.items():

            for keyword in keywords:

                if keyword in text:

                    found.append(

                        Requirement(

                            requirement,

                            1.0

                        )

                    )

                    break

        return found