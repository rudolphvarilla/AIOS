"""
===========================================================
AIOS Search Evidence
core/search/evidence.py
===========================================================

Open-world evidence extraction from search-result text.

This module deliberately does NOT define a closed list of weather,
travel, engineering, or other domain facts. It extracts answer-bearing
measurements and preserves the source wording around them.

Design principles
-----------------
• The source remains authoritative.
• Unknown terminology is preserved rather than discarded.
• Numeric values and units are extracted generically.
• The raw source sentence is retained for later LLM interpretation.
• No value is inferred when the source does not state it.

Version 1.0
===========================================================
"""

from dataclasses import dataclass, field
import re


@dataclass
class SearchFact:
    """A source-grounded observation extracted from a search result."""

    raw_text: str
    source_url: str
    subject: str = ""
    predicate: str = ""
    value: str = ""
    unit: str = ""
    temporal_scope: str = ""
    location: str = ""
    qualifiers: dict = field(default_factory=dict)
    confidence: float = 1.0

    def __str__(self):
        if self.predicate and self.value:
            value = f"{self.value}{(' ' + self.unit) if self.unit else ''}"
            return f"{self.predicate}: {value} | {self.raw_text}"
        return self.raw_text


class DeterministicEvidenceExtractor:
    """Extract source-grounded evidence without a domain-specific ontology."""

    # Number + common unit. The unit list is intentionally measurement-oriented,
    # not weather-oriented, so the same extractor can work across domains.
    MEASUREMENT_PATTERN = re.compile(
        r"(?P<value>[+-]?(?:\d+(?:\.\d+)?|\.\d+))\s*"
        r"(?P<unit>%|°\s*[CF]|\b(?:C|F|mm|cm|km|m|in|inch|inches|ft|feet|mi|miles|"
        r"km/h|kph|mph|m/s|knots?|kt|hPa|Pa|kPa|bar|psi|kg|g|lb|lbs|L|l|mL|ml|"
        r"hours?|hrs?|minutes?|mins?|seconds?|days?|weeks?|months?|years?)\b)",
        re.IGNORECASE,
    )

    TEMPORAL_TERMS = (
        "currently", "current", "now", "today", "tonight", "tomorrow",
        "yesterday", "this week", "next week", "last week", "this month",
        "next month", "last month", "recently", "latest", "present",
    )

    DATE_PATTERN = re.compile(
        r"\b(?:\d{4}-\d{1,2}-\d{1,2}|"
        r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
        r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|"
        r"Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:,\s*\d{4})?)\b",
        re.IGNORECASE,
    )

    SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")

    def extract(self, results):
        facts = []

        for result in results:
            text = f"{result.title}\n{result.snippet}".strip()
            facts.extend(self.extract_from_text(text, result.url))

        return facts

    def extract_from_text(self, text, source_url):
        facts = []
        sentences = [s.strip() for s in self.SENTENCE_SPLIT.split(text) if s.strip()]

        for sentence in sentences:
            measurements = list(self.MEASUREMENT_PATTERN.finditer(sentence))

            for match in measurements:
                value = match.group("value")
                unit = re.sub(r"\s+", "", match.group("unit"))
                predicate = self._infer_predicate(sentence, match.start())
                temporal_scope = self._temporal_scope(sentence)

                facts.append(
                    SearchFact(
                        raw_text=sentence,
                        source_url=source_url,
                        predicate=predicate,
                        value=value,
                        unit=unit,
                        temporal_scope=temporal_scope,
                        qualifiers={"extraction": "deterministic_measurement"},
                    )
                )

            # Preserve explicit dates even when there is no measurement.
            for match in self.DATE_PATTERN.finditer(sentence):
                facts.append(
                    SearchFact(
                        raw_text=sentence,
                        source_url=source_url,
                        predicate="date_reference",
                        value=match.group(0),
                        temporal_scope="explicit",
                        qualifiers={"extraction": "deterministic_date"},
                    )
                )

            # Preserve source wording containing temporal markers even when it
            # has no number. This is deliberately open-ended: unfamiliar terms
            # such as "low pressure area" or "fresh powder" remain available
            # for later semantic interpretation.
            lowered = sentence.casefold()
            if any(term in lowered for term in self.TEMPORAL_TERMS):
                if not measurements and not self.DATE_PATTERN.search(sentence):
                    facts.append(
                        SearchFact(
                            raw_text=sentence,
                            source_url=source_url,
                            predicate="temporal_statement",
                            temporal_scope=self._temporal_scope(sentence),
                            qualifiers={"extraction": "deterministic_temporal_clause"},
                        )
                    )

        return self._deduplicate(facts)

    def _infer_predicate(self, sentence, value_start):
        """Derive a descriptive predicate from nearby source wording only."""
        prefix = sentence[max(0, value_start - 80):value_start].strip().casefold()
        words = re.findall(r"[a-z][a-z_\-/ ]*", prefix)
        nearby = words[-1].strip() if words else "measurement"

        # Generic normalization of obvious grammatical forms. This is not a
        # domain ontology; the original sentence remains in raw_text.
        if "chance of" in prefix or "probability" in prefix:
            return "probability"
        if "temperature" in prefix or "temp" in prefix:
            return "temperature"
        if "wind" in prefix:
            return "wind_measurement"
        if "snow" in prefix:
            return "snow_measurement"
        if "rain" in prefix or "precipitation" in prefix:
            return "precipitation_measurement"
        if "pressure" in prefix:
            return "pressure_measurement"

        return nearby or "measurement"

    def _temporal_scope(self, sentence):
        lowered = sentence.casefold()
        for term in self.TEMPORAL_TERMS:
            if term in lowered:
                return term
        return ""

    def _deduplicate(self, facts):
        seen = set()
        unique = []
        for fact in facts:
            key = (
                fact.source_url,
                fact.raw_text,
                fact.predicate,
                fact.value,
                fact.unit,
            )
            if key in seen:
                continue
            seen.add(key)
            unique.append(fact)
        return unique
