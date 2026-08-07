"""
===========================================================
AIOS Deterministic Search Fact Extractor
core/search/fact_extractor.py
===========================================================

Extracts answer-bearing fact candidates directly from retrieved
search-result text.

Design goals
------------
* deterministic: no LLM call and no closed weather-fact vocabulary
* open-world: unfamiliar nouns/jargon remain in the raw evidence
* provenance-preserving: every fact keeps URL and source sentence
* conservative: extraction creates candidates; it never asserts that
  an extracted value is true beyond what the source text says

Phase 3.1.15
===========================================================
"""

from __future__ import annotations

import re

from core.search.knowledge import SearchFact


class SearchFactExtractor:
    """Extract deterministic, source-grounded fact candidates."""

    # Generic numeric value + unit. The unit is intentionally open-ended so
    # new domains do not require a new weather/engineering vocabulary entry.
    MEASUREMENT_PATTERN = re.compile(
        r"(?P<value>\d+(?:\.\d+)?)\s*"
        r"(?P<unit>°[CF]|[%]|[A-Za-zµμ]+(?:/[A-Za-zµμ]+)?|[A-Za-zµμ]+\^[0-9]+)"
        r"(?=\b|\s|[,.;:!?]|$)",
        re.IGNORECASE,
    )

    # Common grammatical anchors. These describe sentence structure rather
    # than domain vocabulary, so the extracted subject/value may be anything.
    ASSERTION_PATTERN = re.compile(
        r"\b(?:is|are|was|were|has|have|had|shows|showing|reported|reports|"
        r"currently|expected|forecast|measured|recorded|reached|affecting|"
        r"includes|including|contains|stands at|up to|around|about)\b",
        re.IGNORECASE,
    )

    SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")

    def extract(self, results) -> list[SearchFact]:
        facts: list[SearchFact] = []
        seen: set[tuple[str, str, str]] = set()

        for result in results or []:
            source = str(getattr(result, "url", "") or "")
            title = str(getattr(result, "title", "") or "").strip()
            snippet = str(getattr(result, "snippet", "") or "").strip()

            for text in (title, snippet):
                for sentence in self._sentences(text):
                    facts.extend(self._extract_sentence(sentence, source, seen))

        return facts

    def _extract_sentence(self, sentence: str, source: str, seen: set):
        results = []
        sentence = self._clean(sentence)
        if not sentence:
            return results

        measurements = list(self.MEASUREMENT_PATTERN.finditer(sentence))

        for match in measurements:
            value = f"{match.group('value')}{match.group('unit')}"
            subject = self._subject_before(sentence, match.start())
            predicate = self._predicate(sentence, match.start())
            key = (subject.casefold(), predicate.casefold(), value.casefold())

            if key in seen:
                continue

            seen.add(key)
            results.append(
                SearchFact(
                    subject=subject or "source statement",
                    predicate=predicate or "has value",
                    value=value,
                    source=source,
                    evidence=sentence,
                    fact_type="measurement",
                    confidence=1.0,
                )
            )

        # A source can contain useful qualitative information without a
        # numeric value. Preserve the entire source sentence instead of
        # forcing unfamiliar terminology into a fixed domain vocabulary.
        if not measurements and self.ASSERTION_PATTERN.search(sentence):
            assertion = self.ASSERTION_PATTERN.search(sentence)
            subject = self._subject_before(sentence, assertion.start())
            predicate = self._predicate_from_assertion(sentence)
            value = sentence
            key = (subject.casefold(), predicate.casefold(), value.casefold())

            if key not in seen and len(sentence.split()) >= 4:
                seen.add(key)
                results.append(
                    SearchFact(
                        subject=subject or "source statement",
                        predicate=predicate or "reports",
                        value=value,
                        source=source,
                        evidence=sentence,
                        fact_type="statement",
                        confidence=0.85,
                    )
                )

        return results

    def _sentences(self, text: str):
        return [part.strip() for part in self.SENTENCE_SPLIT.split(text) if part.strip()]

    def _clean(self, sentence: str):
        return re.sub(r"\s+", " ", sentence).strip(" -•")

    def _subject_before(self, sentence: str, position: int):
        prefix = sentence[:position].strip(" ,:;-—")
        if not prefix:
            return ""

        # Keep the local noun phrase instead of returning the entire page title.
        words = prefix.split()
        anchors = {
            "in", "at", "for", "from", "with", "of", "and", "the",
            "a", "an", "is", "are", "was", "were", "currently",
            "expected", "reported", "forecast", "conditions", "condition",
        }
        kept = []
        for word in reversed(words):
            if len(kept) >= 5:
                break
            if word.casefold() in anchors and kept:
                break
            kept.append(word)
        return " ".join(reversed(kept)).strip(" ,:;-—")

    def _predicate(self, sentence: str, position: int):
        prefix = sentence[:position].lower()
        for phrase in (
            "chance of",
            "probability of",
            "wind at",
            "winds at",
            "temperature of",
            "temperature at",
            "humidity of",
            "rainfall of",
            "precipitation of",
        ):
            if prefix.endswith(phrase):
                return phrase
        return "has value"

    def _predicate_from_assertion(self, sentence: str):
        match = self.ASSERTION_PATTERN.search(sentence)
        if not match:
            return "reports"
        return match.group(0).lower()
