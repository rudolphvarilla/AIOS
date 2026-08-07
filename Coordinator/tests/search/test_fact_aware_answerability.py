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
