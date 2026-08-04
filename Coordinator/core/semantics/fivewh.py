"""
===========================================================
AIOS 5WH Semantic Understanding
core/semantics/fivewh.py
===========================================================

Extracts the user's information need into six semantic slots:

WHO  - actor / subject affected by the request
WHAT - requested information or action
WHEN - temporal scope
WHERE- geographic / contextual scope
WHY  - explicit purpose or reason
HOW  - requested method, format, or constraints

This module is intentionally a small first validation layer.
It does not answer the user's question and does not judge search
quality by itself. Search validation is performed after retrieval.

Version 1.0 - Phase 3.1.12
===========================================================
"""

from dataclasses import dataclass, field
import json
import re


SCHEMA = """
{
  "who": "",
  "what": "",
  "when": "",
  "where": "",
  "why": "",
  "how": "",
  "confidence": 0.0
}
"""


@dataclass
class FiveWHResult:

    who: str = ""
    what: str = ""
    when: str = ""
    where: str = ""
    why: str = "none provided"
    how: str = "none provided"
    confidence: float = 0.0
    notes: list[str] = field(default_factory=list)

    @classmethod
    def empty(cls):
        return cls()

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        for key in ("who", "what", "when", "where", "why", "how", "confidence"):
            if key in data:
                setattr(obj, key, data[key])
        if not obj.why:
            obj.why = "none provided"
        if not obj.how:
            obj.how = "none provided"
        return obj

    def to_dict(self):
        return {
            "who": self.who,
            "what": self.what,
            "when": self.when,
            "where": self.where,
            "why": self.why,
            "how": self.how,
            "confidence": self.confidence,
        }


class FiveWHUnderstanding:

    def __init__(self, model_manager):
        self.model_manager = model_manager

    def understand(self, query, repository=None, memory=None):
        config = self.model_manager.get("qwen2.5:1.5b")

        if config is None:
            return self.empty_result(query)

        prompt = self.build_prompt(query)
        raw = config.wrapper.generate(prompt)

        return self.parse(raw, query)

    def build_prompt(self, query):
        return f"""
You are AIOS 5WH Semantic Understanding.

Your job is NOT to answer the user.
Your job is to identify what information the user is asking AIOS to obtain.

Return ONLY valid JSON using this schema:

{SCHEMA}

Definitions:

who
The actor, person, group, or subject affected by the request.
If the request is simply made by the user and no other actor matters, use "user".
Do not invent people or groups.

what
The concrete information, task, object, or action requested.

when
The time, date, date range, season, recurrence, or temporal condition requested.
If no temporal scope is present, use "none provided".

where
The geographic location or contextual scope requested.
If no location is present, use "none provided".

why
The explicit purpose or reason stated by the user.
If no purpose is stated, use "none provided".
Never invent a purpose.

how
The requested method, format, comparison, constraints, or level of detail.
Examples: "forecast", "step-by-step", "compare options", "brief summary".
If no method or format is requested, use "none provided".
Never invent a method.

confidence
Your confidence that the six fields correctly represent the user's request.
0.0 = unusable interpretation
1.0 = very clear interpretation

Important:
- Preserve explicit locations and dates.
- Do not turn general knowledge into a user requirement.
- Do not answer the question.
- Do not add recommendations.

User request:
{query}

Return ONLY JSON.
"""

    def parse(self, raw, query=""):
        try:
            cleaned = self.clean_json(raw)
            data = json.loads(cleaned)
            result = FiveWHResult.from_dict(data)
            return self.normalize(result, query)
        except Exception:
            return self.empty_result(query)

    def clean_json(self, text):
        text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            return "{}"
        return text[start:end + 1]

    def normalize(self, result, query=""):
        result.confidence = max(0.0, min(1.0, float(result.confidence or 0.0)))

        for field_name in ("who", "what", "when", "where", "why", "how"):
            value = getattr(result, field_name)
            if value is None or not str(value).strip():
                setattr(result, field_name, "none provided")
            else:
                setattr(result, field_name, str(value).strip())

        if result.who == "none provided":
            result.who = "user"

        return result

    def empty_result(self, query=""):
        return FiveWHResult(
            who="user",
            what="none provided",
            when="none provided",
            where="none provided",
            why="none provided",
            how="none provided",
            confidence=0.0,
            notes=["5WH model unavailable or failed to parse"],
        )
