"""
===========================================================
AIOS Search Candidate Validator
core/search/candidate_validator.py
===========================================================

Filters noisy entity candidates before classification.

Responsibilities

• Reject obvious garbage
• Reject stopword-only phrases
• Reject descriptive phrases
• Keep extractor semantic-free

Version 1.0
===========================================================
"""


class CandidateValidator:

    REJECT_WORDS = {

        "best",
        "top",
        "view",
        "offer",
        "offers",
        "special",
        "find",
        "functional",
        "this",
        "that",
        "these",
        "those",
        "value",
        "review",
        "reviews",
        "traveler",
        "travelers",
        "travellers",
        "tripadvisor",

    }

    # --------------------------------------------------

    def validate(self, candidate):

        words = candidate.split()

        if not words:

            return False

        useful = []

        for word in words:

            if word.casefold() in self.REJECT_WORDS:

                continue

            useful.append(word)

        if not useful:

            return False

        if len(useful) == 1:

            if len(useful[0]) <= 2:

                return False

        return True