"""
===========================================================
AIOS 5WH Search Validator
core/search/fivewh_validator.py
===========================================================

Compares the user's 5WH semantic request against the knowledge
retrieved by the Search Pipeline.

Phase 3.1.12

The validator is an answerability gate, not a factual-truth checker.
It asks whether the retrieved evidence actually addresses the requested
5WH slots instead of treating topical relevance as sufficient evidence.

Version 1.1 - Phase 3.1.12 evidence alignment
===========================================================
"""

from dataclasses import dataclass, field
import re


@dataclass
class FiveWHAlignment:

    score: float = 0.0
    slot_scores: dict[str, float] = field(default_factory=dict)
    missing: list[str] = field(default_factory=list)
    reason: str = ""


class FiveWHValidator:

    WEIGHTS = {
        "who": 0.05,
        "what": 0.35,
        "when": 0.15,
        "where": 0.20,
        "why": 0.10,
        "how": 0.15,
    }

    NONE_VALUES = {
        "", "none", "none provided", "not provided", "n/a", "unknown"
    }

    # Terms that indicate actual weather-condition evidence rather than
    # merely weather-related discussion (e.g. weather systems or hazards).
    WEATHER_EVIDENCE = {
        "temperature", "temp", "celsius", "fahrenheit", "°c", "°f",
        "rain", "rainfall", "rainy", "precipitation", "showers",
        "storm", "storms", "thunderstorm", "cloud", "cloudy",
        "humidity", "wind", "winds", "windy", "forecast", "conditions",
        "sunny", "partly", "overcast", "weather",
    }

    # Terms that indicate an actual current observation/report. A bare
    # "forecast" is intentionally not enough for a request for "now".
    CURRENT_EVIDENCE = {
        "current", "now", "today", "currently", "latest", "observed",
        "observation", "observations", "present", "conditions",
    }

    def validate(self, fivewh, search_context):
        evidence = self._evidence(search_context)
        scores = {}
        missing = []

        for slot in self.WEIGHTS:
            value = getattr(fivewh, slot, "")
            score = self._score_slot(slot, value, evidence)
            scores[slot] = score

            # Only explicit user requirements should create a missing slot.
            if not self._is_none(value) and score < 0.50:
                missing.append(slot)

        score = sum(scores[k] * self.WEIGHTS[k] for k in self.WEIGHTS)

        # A model parse with very low confidence should never create a
        # strong validation result merely because the search contains text.
        score *= max(
            0.50,
            min(1.0, float(getattr(fivewh, "confidence", 0.0) or 0.0) + 0.50),
        )
        score = min(1.0, score)

        if missing:
            reason = "Missing 5WH evidence: " + ", ".join(missing)
        else:
            reason = "5WH request aligned with search context"

        return FiveWHAlignment(
            score=score,
            slot_scores=scores,
            missing=missing,
            reason=reason,
        )

    def _evidence(self, context):
        parts = [
            getattr(context, "topic", ""),
            getattr(context, "summary", ""),
        ]

        for name in (
            "entities",
            "locations",
            "attributes",
            "facts",
            "recommendations",
        ):
            value = getattr(context, name, []) or []
            if isinstance(value, dict):
                parts.extend(str(k) for k in value.keys())
                parts.extend(str(v) for v in value.values())
            else:
                parts.extend(str(item) for item in value)

        return " ".join(parts).lower()

    def _score_slot(self, slot, value, evidence):
        if self._is_none(value):
            return 1.0

        text = str(value).strip().lower()

        if slot == "who" and text == "user":
            return 1.0

        if slot == "what":
            return self._score_what(text, evidence)

        if slot == "when":
            return self._score_when(text, evidence)

        if slot == "where":
            return self._location_match(text, evidence)

        if slot == "how":
            return self._score_how(text, evidence)

        tokens = self._tokens(text)
        if not tokens:
            return 1.0

        hits = sum(1 for token in tokens if token in evidence)
        return min(1.0, hits / max(1, len(tokens)))

    def _score_what(self, text, evidence):
        tokens = self._tokens(text)
        if not tokens:
            return 1.0

        hits = sum(1 for token in tokens if token in evidence)
        lexical = hits / max(1, len(tokens))

        # Weather queries need evidence of actual weather conditions, not
        # merely meteorological topics such as LPAs or monsoon systems.
        if "weather" in tokens:
            weather_hits = sum(
                1 for term in self.WEATHER_EVIDENCE if term in evidence
            )
            if weather_hits == 0:
                return 0.0
            lexical = max(lexical, min(1.0, weather_hits / 3.0))

        return min(1.0, lexical)

    def _score_when(self, text, evidence):
        if any(x in text for x in ("current", "now", "today", "latest", "right now")):
            # Current requests require current-observation language AND
            # condition evidence. "Forecast" alone is future-looking and
            # therefore cannot satisfy "now".
            has_current = any(x in evidence for x in self.CURRENT_EVIDENCE)
            has_weather = any(x in evidence for x in self.WEATHER_EVIDENCE)
            return 1.0 if has_current and has_weather else 0.0

        months = (
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december",
        )
        if any(m in text for m in months):
            return 1.0 if any(m in evidence for m in months if m in text) else 0.0

        years = re.findall(r"20\d{2}", text)
        if years:
            return 1.0 if any(year in evidence for year in years) else 0.0

        return 0.5 if any(t in evidence for t in self._tokens(text)) else 0.0

    def _score_how(self, text, evidence):
        tokens = self._tokens(text)
        if not tokens:
            return 1.0

        hits = sum(1 for token in tokens if token in evidence)
        lexical = hits / max(1, len(tokens))

        if "forecast" in tokens:
            return 1.0 if "forecast" in evidence else 0.0

        return min(1.0, lexical)

    def _tokens(self, text):
        stop = {
            "the", "a", "an", "in", "on", "at", "for", "to", "of",
            "and", "or", "is", "are", "be", "this", "that", "user",
        }
        return [
            t
            for t in re.findall(r"[a-z0-9]+", text)
            if t not in stop and len(t) > 2
        ]

    def _location_match(self, text, evidence):
        tokens = self._tokens(text)
        if not tokens:
            return 1.0
        if all(token in evidence for token in tokens):
            return 1.0
        if any(token in evidence for token in tokens):
            return 0.5
        return 0.0

    def _is_none(self, value):
        return str(value or "").strip().lower() in self.NONE_VALUES
