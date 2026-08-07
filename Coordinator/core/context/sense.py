"""
===========================================================
AIOS Ambiguous Sense Resolver
core/context/sense.py
===========================================================

Deterministically resolves words that belong to multiple semantic domains.

The resolver runs after keyword matching and before domain aggregation. It
uses the already available semantic intent plus local lexical context. It
never calls an LLM.

Phase 3.1.15
===========================================================
"""

from __future__ import annotations

import re


class SenseResolver:
    """Resolve ambiguous keyword matches using intent and context."""

    AMBIGUOUS = {
        "current": {
            "temporal": {
                "domain": "time",
                "concept": "temporal_now",
                "cues": {
                    "weather", "forecast", "temperature", "rain", "rainfall",
                    "precipitation", "storm", "humidity", "wind", "today",
                    "tomorrow", "yesterday", "time", "date", "clock", "latest",
                    "now", "currently", "present", "presently",
                },
            },
            "electrical": {
                "domain": "engineering",
                "concept": "electrical",
                "cues": {
                    "voltage", "resistance", "circuit", "ampere", "amperage",
                    "ohm", "ohms", "battery", "charge", "wire", "pcb",
                    "transformer", "inductance", "capacitance", "impedance",
                    "electricity", "electrical", "multimeter", "oscilloscope",
                },
            },
        },
    }

    def resolve(self, text: str, matches: list[dict], semantic=None):
        normalized = self._normalize(text)
        semantic_domains = {
            str(value).lower()
            for value in getattr(semantic, "domains", []) or []
        }
        semantic_concepts = {
            str(value).lower()
            for value in getattr(semantic, "concepts", []) or []
        }

        resolved = []
        for match in matches:
            token = str(match.get("matched", "")).lower()
            senses = self.AMBIGUOUS.get(token)
            if not senses:
                resolved.append(match)
                continue

            scored = []
            for sense_name, sense in senses.items():
                score = 0.0
                score += sum(
                    1.0 for cue in sense["cues"] if re.search(r"\b" + re.escape(cue) + r"\b", normalized)
                )
                if sense["domain"] in semantic_domains:
                    score += 3.0
                if sense["concept"] in semantic_concepts:
                    score += 3.0
                scored.append((score, sense_name, sense))

            scored.sort(key=lambda item: item[0], reverse=True)
            best_score, best_name, best = scored[0]
            second_score = scored[1][0] if len(scored) > 1 else 0.0

            updated = dict(match)
            updated["sense"] = best_name
            updated["sense_score"] = best_score
            updated["sense_margin"] = best_score - second_score

            # Only rewrite the semantic domain when there is actual evidence.
            # A zero-evidence tie remains untouched instead of guessing.
            if best_score > 0.0 and best_score > second_score:
                updated["domain"] = best["domain"]
                updated["concept"] = best["concept"]
                updated["confidence"] = max(
                    float(match.get("confidence", 1.0)),
                    1.0 + min(1.0, best_score / 10.0),
                )
            else:
                updated["sense"] = "ambiguous"

            resolved.append(updated)

        return resolved

    def _normalize(self, text: str):
        return " ".join(re.findall(r"[a-z0-9]+", str(text or "").lower()))
