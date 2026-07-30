"""
===========================================================
AIOS Search Extractor
core/search/extractor.py
===========================================================

Extracts candidate entities from search results.

The extractor does NOT determine entity types.

Classification is performed later by
SearchEntityClassifier.

Version 2.0
===========================================================
"""

import re

from core.search.knowledge import (
    SearchKnowledge,
    SearchEntity,
)
from core.search.candidate_validator import CandidateValidator


class SearchExtractor:

    # --------------------------------------------------
    # Candidate Proper Noun Pattern
    # --------------------------------------------------

    CANDIDATE_PATTERN = re.compile(
        r"\b([A-Z][A-Za-z0-9&'\-]*(?:\s+[A-Z][A-Za-z0-9&'\-]*){0,4})\b"
    )

    def __init__(self):

        self.validator = CandidateValidator()

    # --------------------------------------------------

    def extract(
        self,
        results,
    ):

        knowledge = SearchKnowledge()

        seen = set()

        for result in results:
            text = (
                f"{result.title}\n"
                f"{result.snippet}"
            )

            matches = self.CANDIDATE_PATTERN.findall(text)

            for candidate in matches:

                candidate = candidate.strip()

                # -----------------------------
                # Title Case Validation
                # -----------------------------

                parts = candidate.split()

                # Reject phrases that are entirely uppercase words
                if all(word.isupper() for word in parts):
                    continue

                # Reject single generic capitalized words
                if len(parts) == 1 and len(parts[0]) < 4:
                    continue

                # -----------------------------
                # Ignore very short phrases
                # -----------------------------

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

        return knowledge