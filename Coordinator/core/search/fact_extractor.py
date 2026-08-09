"""
AIOS Deterministic Search Fact Extractor
Phase 3.1.15
"""

from __future__ import annotations

import re

from core.search.knowledge import SearchFact


class SearchFactExtractor:
    """Extract deterministic, source-grounded fact candidates."""

    # Generic numeric value + unit. The unit is intentionally open-ended so
    # new domains do not require a new weather/engineering vocabulary entry.
    MEASUREMENT_PATTERN = re.compile(
        r"(?P<value>\d+(?:\.\d+)?)"
        r"(?P<space>\s*)"
        r"(?P<unit>"
        r"°[CF]"
        r"|%"
        r"|[A-Za-zµμ]+(?:/[A-Za-zµμ]+)+"
        r"|[A-Za-zµμ]+(?:\^[0-9]+)?"
        r")"
        r"(?=\s|[,.;:!?]|$)",
        re.IGNORECASE,
    )

    # Grammatical anchors rather than a closed domain vocabulary. This lets
    # unfamiliar jargon remain in the original source sentence.
    ASSERTION_PATTERN = re.compile(
        r"\b(?:is|are|was|were|has|have|had|shows|showing|reported|reports|"
        r"currently|expected|forecast|measured|recorded|reached|affecting|"
        r"includes|including|contains|stands at|up to|around|about|due to|"
        r"because of|caused by|may be)\b",
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
            unit = match.group("unit")
            # Normalize human-readable units while keeping compact scientific
            # and symbolic units compact: 31km/h -> 31 km/h, 8inches -> 8 inches,
            # while 28°C and 82% remain unchanged.
            separator = "" if unit in {"%", "°C", "°F"} else " "
            value = f"{match.group('value')}{separator}{unit}"
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

        # Preserve the whole sentence even when it also contains a numeric
        # measurement. This is critical for qualifiers such as "due to a low
        # pressure area outside the region" that should not be discarded just
        # because the sentence also contains "80%".
        assertion = self.ASSERTION_PATTERN.search(sentence)
        if assertion and len(sentence.split()) >= 4:
            subject = self._subject_before(sentence, assertion.start())
            predicate = self._predicate_from_assertion(sentence)
            value = sentence
            key = (subject.casefold(), predicate.casefold(), value.casefold())

            if key not in seen:
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
            "chance of", "probability of", "wind at", "winds at",
            "temperature of", "temperature at", "humidity of",
            "rainfall of", "precipitation of",
        ):
            if prefix.endswith(phrase):
                return phrase
        return "has value"

    def _predicate_from_assertion(self, sentence: str):
        match = self.ASSERTION_PATTERN.search(sentence)
        if not match:
            return "reports"
        return match.group(0).lower()
