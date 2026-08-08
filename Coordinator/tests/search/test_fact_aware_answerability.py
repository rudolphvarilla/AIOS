from types import SimpleNamespace

from core.search.fact_extractor import SearchFactExtractor
from core.search.search_context import SearchContextBuilder


def result(title, snippet, url="https://example.com/weather"):
    return SimpleNamespace(title=title, snippet=snippet, url=url)


def fivewh():
    return SimpleNamespace(
        who="user",
        what="weather",
        when="current",
        where="Philippines",
        why="information",
        how="none provided",
        confidence=1.0,
    )


def test_deterministic_facts_make_current_weather_answerable():
    results = [
        result(
            "Philippines Weather",
            "Current conditions: 28°C and 89% chance of rain.",
        )
    ]
    facts = SearchFactExtractor().extract(results)

    knowledge = SimpleNamespace(
        entities=[],
        relations=[],
        recommendations=[],
        categories={},
        locations=[],
        attributes=[],
        facts=[fact.render() for fact in facts],
        fact_records=facts,
    )

    context = SearchContextBuilder().build(
        query="current weather in Philippines",
        results=results,
        knowledge=knowledge,
        summary="Current weather in Philippines.",
        fivewh=fivewh(),
    )

    assert context.fact_records
    assert context.answerability.slot_scores["answer_data"] == 1.0
    assert "answer-bearing data" not in context.answerability.missing


def test_weather_qualifier_is_preserved_without_becoming_an_interpretation():
    results = [
        result(
            "Weather Advisory",
            "Precipitation at 80% may be due to a low pressure area outside the region.",
            url="https://pagasa.dost.gov.ph/weather",
        )
    ]
    facts = SearchFactExtractor().extract(results)

    measurement = next(fact for fact in facts if fact.value == "80%")
    statement = next(
        fact
        for fact in facts
        if fact.fact_type == "statement"
        and "low pressure area outside the region" in fact.evidence.lower()
    )

    assert measurement.source == "https://pagasa.dost.gov.ph/weather"
    assert measurement.evidence == statement.evidence
    assert statement.source == "https://pagasa.dost.gov.ph/weather"
    assert statement.value == statement.evidence
    assert "may be due to" in statement.evidence.lower()
    assert "caused by" not in statement.value.lower()
