"""
===========================================================
AIOS Search Extractor
core/search/extractor.py
===========================================================

Extracts candidate entities and source-grounded evidence from search results.

The extractor does NOT determine entity types or truth. It preserves what the
source actually says so later semantic and deterministic layers can reason
about it without inventing missing information.

Version 2.1
===========================================================
"""

import re

from core.search.knowledge import (
    SearchKnowledge,
    SearchEntity,
)
from core.search.candidate_validator import CandidateValidator
from core.search.evidence import DeterministicEvidenceExtractor


class SearchExtractor:

    CANDIDATE_PATTERN = re.compile(
        r"\b([A-Z][A-Za-z0-9&'\-]*(?:\s+[A-Z][A-Za-z0-9&'\-]*){0,4})\b"
    )

    def __init__(self):
        self.validator = CandidateValidator()
        self.evidence = DeterministicEvidenceExtractor()

    def extract(self, results):
        knowledge = SearchKnowledge()

        seen = set()

        for result in results:
            text = f"{result.title}\n{result.snippet}"

            # ---------------------------------------------
            # Source-grounded evidence
            # ---------------------------------------------
            knowledge.facts.extend(
                self.evidence.extract_from_text(
                    text,
                    result.url,
                )
            )

            # ---------------------------------------------
            # Candidate entities
            # ---------------------------------------------
            matches = self.CANDIDATE_PATTERN.findall(text)

            for candidate in matches:
                candidate = candidate.strip()
                parts = candidate.split()

                if all(word.isupper() for word in parts):
                    continue

                if len(parts) == 1 and len(parts[0]) < 4:
                    continue

                if len(candidate) < 3:
                    continue

                if not self.validator.validate(candidate):
                    continue

                key = candidate.casefold()

                if key in seen:
                    continue

                seen.add(key)

                knowledge.entities.append(
                    SearchEntity(
                        name=candidate,
                        entity_type="UNKNOWN",
                        source=result.url,
                    )
                )

        print("\n===== EXTRACTED CANDIDATES =====")
        for entity in knowledge.entities:
            print(entity.name)

        print("\n===== EXTRACTED EVIDENCE =====")
        for fact in knowledge.facts:
            print(f" - {fact}")

        return knowledge
