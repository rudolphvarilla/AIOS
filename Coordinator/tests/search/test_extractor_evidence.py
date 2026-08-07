from types import SimpleNamespace

from core.search.extractor import SearchExtractor


def test_search_extractor_keeps_answer_bearing_values_in_knowledge_facts():
    results = [
        SimpleNamespace(
            title="Philippines Current Weather",
            snippet=(
                "Forecast is 28 °C with a 89% chance of rain. "
                "Wind at 31 km/h."
            ),
            url="https://example.test/weather",
        )
    ]

    knowledge = SearchExtractor().extract(results)

    values = {(fact.value, fact.unit) for fact in knowledge.facts}

    assert ("28", "°C") in values
    assert ("89", "%") in values
    assert ("31", "km/h") in values
