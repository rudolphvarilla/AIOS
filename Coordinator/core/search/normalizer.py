"""
===========================================================
AIOS Search Knowledge Normalizer
core/search/normalizer.py
===========================================================

Normalizes extracted entities.

Responsibilities

• Remove stopwords
• Remove duplicates
• Standardize names

Version 1.1
===========================================================
"""

import re


STOPWORDS = {

    "THE",
    "BEST",
    "TOP",
    "HOTEL",
    "HOTELS",
    "AND",
    "OF",
    "IN",
    "FOR",

}


class SearchNormalizer:

    # -------------------------------------------------

    def normalize(self, entities):

        cleaned = []

        seen = set()

        for entity in entities:

            name = self.clean(entity.name)

            if not name:

                continue

            if name.lower() in seen:

                continue

            seen.add(name.lower())

            entity.name = name

            cleaned.append(entity)

        return cleaned

    # -------------------------------------------------

    def clean(self, text):

        text = text.strip()

        text = re.sub(r"\s+", " ", text)

        words = []

        for word in text.split():

            if word.upper() in STOPWORDS:

                continue

            words.append(word)

        return " ".join(words)