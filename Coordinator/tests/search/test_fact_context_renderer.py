from types import SimpleNamespace

from core.search.context_renderer import SearchContextRenderer
from core.search.knowledge import SearchFact


def test_renderer_preserves_fact_evidence_qualifiers_and_source():
    fact = SearchFact(
        subject="precipitation",
        predicate="may be",
        value="Precipitation at 80% may be due to a low pressure area outside the region.",
        source="https://example.com/weather",
        evidence="Precipitation at 80% may be due to a low pressure area outside the region.",
        fact_type="statement",
        confidence=0.85,
    )

    context = SimpleNamespace(
        topic="current weather",
        summary="Current weather report.",
        entities=[],
        relations=[],
        recommendations=[],
        fact_records=[fact],
        sources=[fact.source],
        confidence=0.90,
    )

    rendered = SearchContextRenderer().render(context)

    assert "SOURCE-GROUNDED FACTS" in rendered
    assert fact.evidence in rendered
    assert fact.source in rendered
    assert "Preserve epistemic wording" in rendered
    assert "may be" in rendered
    assert "do not upgrade qualifiers" in rendered


def test_renderer_does_not_create_fact_interpretations():
    fact = SearchFact(
        subject="weather",
        predicate="reports",
        value="Overnight snowfall produced 8 inches of new powder.",
        source="https://example.com/mountain",
        evidence="Overnight snowfall produced 8 inches of new powder.",
        fact_type="statement",
        confidence=0.85,
    )

    context = SimpleNamespace(
        topic="snowfall",
        summary="Mountain report.",
        entities=[],
        relations=[],
        recommendations=[],
        fact_records=[fact],
        sources=[fact.source],
        confidence=0.90,
    )

    rendered = SearchContextRenderer().render(context)

    assert "8 inches of new powder" in rendered
    assert "SOURCE-GROUNDED FACTS" in rendered
    assert "caused by" not in rendered
    assert "therefore" not in rendered.lower()
