"""
===========================================================
AIOS Entity Detector
core/perception/analyzers/entity_detector.py
===========================================================

Detects entities mentioned by the user.

Responsibilities

• Extract entities from text
• Assign simple labels
• Return detected entities

This module performs lexical detection only.

No repository lookup.
No AI.
No search.

Future

- Repository entities
- Knowledge graph entities
- Named Entity Recognition
- LLM entity extraction

Version
1.0
===========================================================
"""

from dataclasses import dataclass

import re
from core.keywords.lexicon.entities import ENTITY_KEYWORDS
from core.keywords.tools.normalizer import KeywordNormalizer

# ---------------------------------------------------------
# Entity Object
# ---------------------------------------------------------

@dataclass
class Entity:

    text: str

    label: str

    confidence: float


# ---------------------------------------------------------
# Entity Detector
# ---------------------------------------------------------

class EntityDetector:

    def __init__(self):

        self.normalizer = KeywordNormalizer()

    def detect(self, text):

        text = self.normalizer.normalize(text)

        entities = []

        for keyword, label in ENTITY_KEYWORDS.items():

            pattern = r"\b" + re.escape(keyword) + r"\b"

            match = re.search(pattern, text)

            if match is None:

                continue

            entities.append(

                Entity(

                    text=keyword,

                    label=label,

                    confidence=1.0,

                )

            )

        return entities