"""
===========================================================
AIOS Semantic Test Helper
tests/semantics/helper.py
===========================================================

Shared helper for Semantic Registry tests.

Every semantic test imports this helper.

Version 1
===========================================================
"""

from core.context.engine import ContextEngine


engine = ContextEngine()


def match(text: str):

    result = engine.analyze(text)

    return result.matches


def assert_detected(domain: str, text: str):

    matches = match(text)

    assert any(
        item["domain"] == domain
        for item in matches
    ), f"{domain} not detected for '{text}'"


def assert_not_detected(domain: str, text: str):

    matches = match(text)

    assert not any(
        item["domain"] == domain
        for item in matches
    ), f"{domain} incorrectly detected for '{text}'"