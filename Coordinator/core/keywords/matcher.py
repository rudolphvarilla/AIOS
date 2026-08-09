"""
===========================================================
AIOS Keyword Matcher
core/keywords/matcher.py
===========================================================

Matches user text against semantic registries and reweights ambiguous words
using already-extracted semantic intent.

Version 3.2
===========================================================
"""

import re

from core.keywords.loader import KeywordLoader
from core.keywords.tools.normalizer import KeywordNormalizer
from core.keywords.sense_resolver import SenseResolver


class KeywordMatcher:

    def __init__(self):
        self.loader = KeywordLoader()
        self.normalizer = KeywordNormalizer()
        self.sense_resolver = SenseResolver()

    def _weight(self, phrase: str) -> float:
        return float(len(phrase.split()))

    def match(self, text: str, semantic=None):
        original_text = text
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
                    ambiguous = keyword.casefold() in self.sense_resolver.AMBIGUOUS

                    contained = False
                    for s, e in matched_spans:
                        if start >= s and end <= e:
                            contained = True
                            break

                    # Multiple registries are intentionally allowed to match
                    # the same span for ambiguous terms. The sense resolver
                    # then decides which meaning is supported by intent.
                    if contained and not ambiguous:
                        continue

                    if not ambiguous:
                        matched_spans.append((start, end))

                    match = {
                        "domain": registry_name.lower(),
                        "concept": concept,
                        "matched": keyword,
                        "confidence": base_confidence * self._weight(keyword),
                    }

                    if semantic is not None:
                        match = self.sense_resolver.adjust(
                            match,
                            semantic,
                            original_text,
                        )

                    matches.append(match)

        matches.sort(
            key=lambda x: x["confidence"],
            reverse=True,
        )

        return matches
