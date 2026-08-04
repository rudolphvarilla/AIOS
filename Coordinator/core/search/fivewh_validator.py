"""
===========================================================
AIOS 5WH Search Validator
core/search/fivewh_validator.py
===========================================================

Compares the user's 5WH semantic request against the knowledge
retrieved by the Search Pipeline.

This is the first search-answerability gate for Phase 3.1.12.
It validates alignment, not factual truth. Later phases can replace
this lightweight lexical evidence check with richer evidence alignment.

Version 1.0 - Phase 3.1.12
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

    NONE_VALUES = {"", "none", "none provided", "not provided", "n/a", "unknown"}

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
        score *= max(0.50, min(1.0, float(getattr(fivewh, "confidence", 0.0) or 0.0) + 0.50))
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

        for name in ("entities", "locations", "attributes", "facts", "recommendations"):
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

        tokens = self._tokens(text)
        if not tokens:
            return 1.0

        hits = sum(1 for token in tokens if token in evidence)
        base = hits / max(1, len(tokens))

        if slot == "when":
            base = max(base, self._temporal_match(text, evidence))

        if slot == "where":
            base = max(base, self._location_match(text, evidence))

        return min(1.0, base)

    def _tokens(self, text):
        stop = {
            "the", "a", "an", "in", "on", "at", "for", "to", "of",
            "and", "or", "is", "are", "be", "this", "that", "user",
        }
        return [t for t in re.findall(r"[a-z0-9]+", text) if t not in stop and len(t) > 2]

    def _temporal_match(self, text, evidence):
        if any(x in text for x in ("current", "now", "today", "latest", "right now")):
            if any(x in evidence for x in ("current", "today", "now", "latest", "updated", "issued", "forecast")):
                return 1.0
            return 0.25

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
