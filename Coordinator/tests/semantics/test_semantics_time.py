"""
AIOS Semantic Test
Time Registry
"""

from tests.semantics.helper import (
    assert_detected,
    assert_not_detected,
)


def test_relative_days():

    assert_detected("time", "today")
    assert_detected("time", "tomorrow")
    assert_detected("time", "yesterday")


def test_weeks():

    assert_detected("time", "next week")
    assert_detected("time", "last week")


def test_months():

    assert_detected("time", "this month")


def test_weekdays():

    assert_detected("time", "monday")
    assert_detected("time", "friday")


def test_negative():

    assert_not_detected("time", "camera")
    assert_not_detected("time", "airport")
    assert_not_detected("time", "motorcycle")

def test_case_insensitive():

    assert_detected("time", "Tomorrow")
    assert_detected("time", "TOMORROW")
    assert_detected("time", "Tomorrow!")
    assert_detected("time", "Tomorrow morning")