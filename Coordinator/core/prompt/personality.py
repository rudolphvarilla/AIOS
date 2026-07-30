"""
===========================================================
AIOS Personality Prompt
core/prompt/personality.py
===========================================================

Selectable behavioral layer.

This block modifies HOW the model responds.

It never changes factual information.

Version 1

Future Personalities
--------------------
• Default
• Coding
• Research
• Teacher
• Photography
• Aviation
• Travel
"""

PERSONALITIES = {
    "default": "",
    "coding": "",
    "research": "",
    "teacher": "",
    "photography": "",
    "aviation": "",
    "travel": "",
}

class PersonalityPrompt:

    def build(self, personality="default"):

        return PERSONALITIES.get(
            personality,
            PERSONALITIES["default"]
        )