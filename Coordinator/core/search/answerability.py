"""
===========================================================
AIOS Search Answerability Validator
core/search/answerability.py
===========================================================

Determines whether retrieved search evidence is sufficient to answer
the user's request.

This is intentionally different from relevance and 5WH alignment:

• Relevance asks: "Is this about the topic?"
• 5WH alignment asks: "Does it match the requested semantic slots?"
• Answerability asks: "Does the evidence actually contain enough
  answer-bearing information to produce a useful answer?"

Phase 3.1.14
===========================================================
"""

from dataclasses import dataclass, field
import re


@dataclass
class AnswerabilityResult:
    score: float = 0.0
    evidence_score: float = 0.0
    slot_scores: dict[str, float] = field(default_factory=dict)
    missing: list[str] = field(default_factory=list)
    reason: str = ""


class AnswerabilityValidator:
    """Validate answer-bearing evidence without attempting fact checking."""

    WEATHER_TERMS = {
        "weather", "temperature", "temp", "celsius", "fahrenheit",
        "rain", "rainfall", "rainy", "precipitation", "showers",
        "storm", "storms", "thunderstorm", "cloud", "cloudy",
        "humidity", "wind", "winds", "windy", "sunny", "partly",
        "overcast", "conditions",
    }

    CURRENT_TERMS = {
        "current", "now", "currently", "today", "latest", "observed",
        "observation", "observations", "present",
    }

    WEATHER_MEASUREMENT_PATTERNS = (
        r"\b\d+(?:\.\d+)?\s*°\s*[cf]\b",
        r"\b\d+(?:\.\d+)?\s*(?:degrees?|°)\s*(?:c|f|celsius|fahrenheit)\b",
        r"\b\d+(?:\.\d+)?\s*(?:km/h|kph|mph|m/s)\b",
        r"\b\d+(?:\.\d+)?\s*(?:%|percent)\b",
        r"\b\d+(?:\.\d+)?\s*(?:mm|inches?)\s*(?:rain|rainfall|precipitation)?\b",
    )

    def validate(self, fivewh, results, summary=""):
        evidence = self._evidence(results, summary)
        slots = {}
        missing = []

        what = str(getattr(fivewh, "what", "") or "").lower()
        when = str(getattr(fivewh, "when", "") or "").lower()
        where = str(getattr(fivewh, "where", "") or "").lower()

        slots["topic_evidence"] = self._topic_score(what, evidence)
        slots["location_evidence"] = self._location_score(where, evidence)
        slots["time_evidence"] = self._time_score(when, evidence)
        slots["answer_data"] = self._answer_data_score(what, when, evidence)

        if not self._none(what) and slots["topic_evidence"] < 0.50:
            missing.append("topic evidence")
        if not self._none(where) and slots["location_evidence"] < 0.50:
            missing.append("location evidence")
        if not self._none(when) and slots["time_evidence"] < 0.50:
            missing.append("time evidence")
        if slots["answer_data"] < 0.50:
            missing.append("answer-bearing data")

        evidence_score = (
            slots["topic_evidence"] * 0.20
            + slots["location_evidence"] * 0.20
            + slots["time_evidence"] * 0.20
            + slots["answer_data"] * 0.40
        )

        model_confidence = float(getattr(fivewh, "confidence", 0.0) or 0.0)
        score = evidence_score * max(0.50, min(1.0, model_confidence + 0.50))
        score = min(1.0, max(0.0, score))

        if missing:
            reason = "Insufficient answer-bearing evidence: " + ", ".join(missing)
        else:
            reason = "Search evidence is sufficient to answer the request"

        return AnswerabilityResult(
            score=score,
            evidence_score=evidence_score,
            slot_scores=slots,
            missing=missing,
            reason=reason,
        )

    def _evidence(self, results, summary):
        parts = [str(summary or "")]
        for result in results or []:
            parts.extend([
                str(getattr(result, "title", "") or ""),
                str(getattr(result, "snippet", "") or ""),
            ])
        return " ".join(parts).lower()

    def _topic_score(self, value, evidence):
        if self._none(value):
            return 1.0
        tokens = self._tokens(value)
        if not tokens:
            return 1.0
        hits = sum(1 for token in tokens if token in evidence)
        return min(1.0, hits / len(tokens))

    def _location_score(self, value, evidence):
        if self._none(value):
            return 1.0
        tokens = self._tokens(value)
        if not tokens:
            return 1.0
        hits = sum(1 for token in tokens if token in evidence)
        return min(1.0, hits / len(tokens))

    def _time_score(self, value, evidence):
        if self._none(value):
            return 1.0

        if any(term in value for term in ("current", "now", "currently", "today")):
            has_current = any(term in evidence for term in self.CURRENT_TERMS)
            return 1.0 if has_current else 0.0

        years = re.findall(r"20\d{2}", value)
        if years:
            return 1.0 if any(year in evidence for year in years) else 0.0

        months = (
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december",
        )
        requested_months = [month for month in months if month in value]
        if requested_months:
            return 1.0 if any(month in evidence for month in requested_months) else 0.0

        return 0.5

    def _answer_data_score(self, what, when, evidence):
        if "weather" in self._tokens(what):
            weather_hits = sum(1 for term in self.WEATHER_TERMS if term in evidence)
            if weather_hits == 0:
                return 0.0

            is_current = any(
                term in when for term in ("current", "now", "currently", "today")
            )

            if is_current:
                # A generic weather page or forecast landing page is relevant
                # but is not answer-bearing. Current requests require at least
                # one observable quantitative condition or explicit condition.
                has_measurement = any(
                    re.search(pattern, evidence)
                    for pattern in self.WEATHER_MEASUREMENT_PATTERNS
                )
                has_condition = any(
                    term in evidence
                    for term in (
                        "sunny", "cloudy", "overcast", "showers",
                        "thunderstorm", "rainy", "clear skies",
                    )
                )
                return 1.0 if has_measurement or has_condition else 0.0

            has_forecast = "forecast" in evidence or "outlook" in evidence
            return 1.0 if has_forecast and weather_hits >= 1 else 0.50

        # Generic factual requests require enough retrieved text to provide
        # an answer rather than merely naming a matching page.
        return 1.0 if len(evidence.split()) >= 12 else 0.0

    def _tokens(self, value):
        stop = {
            "the", "a", "an", "in", "on", "at", "for", "to", "of",
            "and", "or", "is", "are", "be", "this", "that", "user",
        }
        return [
            token
            for token in re.findall(r"[a-z0-9]+", value)
            if token not in stop and len(token) > 2
        ]

    def _none(self, value):
        return str(value or "").strip().lower() in {
            "", "none", "none provided", "not provided", "n/a", "unknown"
        }
