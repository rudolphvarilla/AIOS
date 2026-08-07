from types import SimpleNamespace

from core.search.fact_extractor import SearchFactExtractor


def result(title, snippet, url="https://example.com/source"):
    return SimpleNamespace(title=title, snippet=snippet, url=url)


def test_extracts_numeric_weather_facts_without_weather_fact_vocabulary():
    facts = SearchFactExtractor().extract([
        result(
            "Philippines Weather",
            "Current conditions: 28°C, humidity 82%, winds 31 km/h, and 89% chance of rain.",
        )
    ])

    values = {fact.value for fact in facts if fact.fact_type == "measurement"}

    assert "28°C" in values
    assert "82%" in values
    assert "31 km/h" in values
    assert "89%" in values
    assert all(fact.source == "https://example.com/source" for fact in facts)
    assert all(fact.evidence for fact in facts)


def test_preserves_unfamiliar_terminology_as_source_grounded_statement():
    facts = SearchFactExtractor().extract([
        result(
            "PAGASA",
            "The southwest monsoon is affecting Central Luzon and the western section of Visayas.",
            url="https://pagasa.dost.gov.ph/weather",
        )
    ])

    assert any(
        "southwest monsoon" in fact.evidence.lower()
        and "visayas" in fact.evidence.lower()
        and fact.source == "https://pagasa.dost.gov.ph/weather"
        for fact in facts
    )


def test_extracts_domain_unknown_measurements_such_as_new_snow():
    facts = SearchFactExtractor().extract([
        result(
            "Mountain Report",
            "Overnight snowfall produced 8 inches of new powder.",
        )
    ])

    assert any(fact.value == "8 inches" for fact in facts)
    assert any("8 inches of new powder" in fact.evidence for fact in facts)
