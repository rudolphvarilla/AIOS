"""
===========================================================
AIOS Keyword Reviewer
core/keywords/tools/reviewer.py
===========================================================

Reviews generated keyword candidates.

Version 1 performs only basic validation.

Checks
• lowercase
• remove duplicates
• remove empty strings
• alphabetical ordering

Future
• AI semantic review
• confidence scoring
• blacklist filtering
• ambiguity detection
• merge similar keywords
• reject hallucinations
===========================================================
"""

class KeywordReviewer:

    def review(self, generated):

        reviewed = {}

        for domain, keywords in generated.items():

            cleaned = set()

            for keyword in keywords:

                if not keyword:
                    continue

                keyword = keyword.strip().lower()

                if keyword:

                    cleaned.add(keyword)

            reviewed[domain] = sorted(cleaned)

        return reviewed