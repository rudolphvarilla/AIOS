"""
===========================================================
AIOS Keyword Matcher
core/keywords/matcher.py
===========================================================

Matches user text against every semantic registry.

Supports:

• Whole-word matching
• Multi-word phrase matching
• Phrase weighting
• Longest phrase preference

Version 3.0
===========================================================
"""

import re

from core.keywords.loader import KeywordLoader
from core.keywords.tools.normalizer import KeywordNormalizer
from core.keywords.lexicon.stopwords import STOPWORDS

class KeywordMatcher:

    def __init__(self):

        self.loader = KeywordLoader()
        self.normalizer = KeywordNormalizer()

    def _weight(self, phrase: str) -> float:
        """
        Multi-word phrases are stronger than single words.

        one word   -> x1
        two words  -> x2
        three      -> x3
        """

        return float(len(phrase.split()))

    def match(self, text: str):

        text = self.normalizer.normalize(text)

        tokens = self.normalizer.tokenize(text)

        text = " ".join(tokens)

        modules = self.loader.load()

        matches = []

        matched_spans = []

        for module in modules:

            registry_name = module.__name__.split(".")[-1].upper()

            if not hasattr(module, registry_name):
                continue

            registry = getattr(module, registry_name)

            if not isinstance(registry, dict):
                continue

            for concept, data in registry.items():

                keywords = sorted(
                    data.get("keywords", set()),
                    key=len,
                    reverse=True,
                )

                base_confidence = data.get("confidence", 1.0)

                for keyword in keywords:

                    pattern = r"\b" + re.escape(keyword) + r"\b"

                    found = re.search(pattern, text)

                    if not found:
                        continue

                    start, end = found.span()

                    # ---------------------------------
                    # Skip if fully contained inside
                    # an already matched longer phrase
                    # ---------------------------------

                    contained = False

                    for s, e in matched_spans:

                        if start >= s and end <= e:
                            contained = True
                            break

                    if contained:
                        continue

                    matched_spans.append((start, end))

                    matches.append({

                        "domain": registry_name.lower(),

                        "concept": concept,

                        "matched": keyword,

                        "confidence":
                            base_confidence * self._weight(keyword)

                    })

        matches.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

        return matches