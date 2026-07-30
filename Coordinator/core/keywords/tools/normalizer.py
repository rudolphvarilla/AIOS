"""
===========================================================
AIOS Keyword Normalizer
core/keywords/tools/normalizer.py
===========================================================

Description

Preprocesses user input before semantic keyword matching.

Responsibilities
----------------
• Lowercase conversion
• Unicode normalization
• Collapse repeated whitespace
• Strip surrounding whitespace

Future
------
• Typo correction
• Learned aliases
• User vocabulary
• Language normalization
• Semantic normalization
• Qdrant-assisted normalization

Version
1.0
===========================================================
"""

import re
import unicodedata
from core.keywords.lexicon.stopwords import STOPWORDS

class KeywordNormalizer:

    def normalize(self, text: str) -> str:

        if text is None:

            return ""

        # ------------------------------------------
        # Unicode normalization
        # ------------------------------------------

        text = unicodedata.normalize("NFKC", text)

        # ------------------------------------------
        # Lowercase
        # ------------------------------------------

        text = text.lower()

        # ------------------------------------------
        # Remove punctuation
        # ------------------------------------------

        text = re.sub(r"[^\w\s]", " ", text)

        # ------------------------------------------
        # Collapse whitespace
        # ------------------------------------------

        text = re.sub(r"\s+", " ", text)

        # ------------------------------------------
        # Strip
        # ------------------------------------------

        text = text.strip()

        return text

    def tokenize(self, text: str):

        text = self.normalize(text)

        return [
            token
            for token in text.split()
            if token not in STOPWORDS
        ]
