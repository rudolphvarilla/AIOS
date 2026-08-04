"""
Phase 3.1.12 - 5WH regression tests.

These tests intentionally avoid an LLM. They validate the deterministic
5WH parsing contract and the first search-alignment gate.
"""

import unittest

from core.semantics.fivewh import FiveWHResult, FiveWHUnderstanding
from core.search.context import SearchContext
from core.search.fivewh_validator import FiveWHValidator


class FiveWHTests(unittest.TestCase):

    def setUp(self):
        self.validator = FiveWHValidator()

    def context(self, summary="", locations=None, facts=None, entities=None):
        return SearchContext(
            topic="test",
            summary=summary,
            locations=locations or [],
            facts=facts or [],
            entities=entities or [],
            confidence=0.9,
        )

    def test_parse_json(self):
        engine = object.__new__(FiveWHUnderstanding)
        result = engine.parse(
            '{"who":"user","what":"weather forecast","when":"September 2026",'
            '"where":"Tokyo","why":"travel planning","how":"forecast",'
            '"confidence":0.9}'
        )

        self.assertEqual(result.who, "user")
        self.assertEqual(result.what, "weather forecast")
        self.assertEqual(result.when, "September 2026")
        self.assertEqual(result.where, "Tokyo")
        self.assertEqual(result.why, "travel planning")
        self.assertEqual(result.how, "forecast")
        self.assertEqual(result.confidence, 0.9)

    def test_explicit_requirements_align(self):
        fivewh = FiveWHResult(
            who="user",
            what="weather forecast",
            when="September 2026",
            where="Tokyo",
            why="none provided",
            how="forecast",
            confidence=1.0,
        )

        context = self.context(
            summary="Tokyo weather forecast for September 2026 with expected temperature and rainfall.",
            locations=["Tokyo"],
            facts=["September 2026 forecast"],
        )

        alignment = self.validator.validate(fivewh, context)

        self.assertGreaterEqual(alignment.score, 0.70)
        self.assertEqual(alignment.missing, [])

    def test_unrelated_results_fail_alignment(self):
        fivewh = FiveWHResult(
            who="user",
            what="weather forecast",
            when="September 2026",
            where="Tokyo",
            why="none provided",
            how="forecast",
            confidence=1.0,
        )

        context = self.context(
            summary="Tokyo hotels, restaurants, museums and train stations.",
            locations=["Tokyo"],
        )

        alignment = self.validator.validate(fivewh, context)

        self.assertLess(alignment.score, 0.70)
        self.assertIn("what", alignment.missing)

    def test_no_explicit_when_where_does_not_penalize(self):
        fivewh = FiveWHResult(
            who="user",
            what="weather",
            when="none provided",
            where="none provided",
            why="none provided",
            how="none provided",
            confidence=1.0,
        )

        context = self.context(
            summary="Current weather conditions and rainfall outlook.",
        )

        alignment = self.validator.validate(fivewh, context)

        self.assertEqual(alignment.slot_scores["when"], 1.0)
        self.assertEqual(alignment.slot_scores["where"], 1.0)


if __name__ == "__main__":
    unittest.main()
