"""
===========================================================
AIOS Fact-Aware Answerability
core/search/fact_aware_answerability.py
===========================================================

Extends the existing answerability contract with deterministic structured
facts extracted from search-result text.

The existing validator remains the compatibility baseline. This layer only
changes answer-data evidence when the extractor has produced source-grounded
measurement or statement facts.
===========================================================
"""

from core.search.answerability import AnswerabilityValidator


class FactAwareAnswerabilityValidator(AnswerabilityValidator):
    """Use structured deterministic facts as answer-bearing evidence."""

    def validate(self, fivewh, results, summary="", facts=None):
        result = super().validate(fivewh, results, summary=summary)
        fact_records = list(facts or [])

        answer_facts = [
            fact for fact in fact_records
            if getattr(fact, "fact_type", "") in {"measurement", "statement"}
            and str(getattr(fact, "evidence", "") or "").strip()
        ]

        if not answer_facts:
            return result

        result.slot_scores["answer_data"] = 1.0
        result.evidence_score = (
            result.slot_scores.get("topic_evidence", 0.0) * 0.20
            + result.slot_scores.get("location_evidence", 0.0) * 0.20
            + result.slot_scores.get("time_evidence", 0.0) * 0.20
            + 0.40
        )

        model_confidence = float(getattr(fivewh, "confidence", 0.0) or 0.0)
        result.score = min(
            1.0,
            max(0.0, result.evidence_score * max(0.50, min(1.0, model_confidence + 0.50))),
        )

        result.missing = [
            item for item in result.missing if item != "answer-bearing data"
        ]

        if result.missing:
            result.reason = "Insufficient answer-bearing evidence: " + ", ".join(result.missing)
        else:
            result.reason = "Search evidence is sufficient to answer the request"

        return result
