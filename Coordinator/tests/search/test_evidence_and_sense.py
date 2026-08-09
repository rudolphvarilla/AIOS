from types import SimpleNamespace

from core.search.evidence import DeterministicEvidenceExtractor
from core.keywords.sense_resolver import SenseResolver


def test_weather_measurements_are_extracted_without_weather_fact_whitelist():
    extractor = DeterministicEvidenceExtractor()

    text = (
        "Today's Weather: 28 °C with a 89% chance of rain. "
        "Wind is expected at 31 km/h."
    )

    facts = extractor.extract_from_text(text, "https://example.test/weather")

    values = {(fact.value, fact.unit) for fact in facts}

    assert ("28", "°C") in values
    assert ("89", "%") in values
    assert ("31", "km/h") in values


def test_unfamiliar_weather_terminology_is_preserved_in_source_sentence():
    extractor = DeterministicEvidenceExtractor()

    text = (
        "Precipitation at 80% could be due to a low pressure area "
        "outside the region."
    )

    facts = extractor.extract_from_text(text, "https://example.test/weather")

    assert any("low pressure area" in fact.raw_text.casefold() for fact in facts)
    assert any(fact.value == "80" and fact.unit == "%" for fact in facts)


def test_current_prefers_temporal_sense_when_semantic_intent_is_weather():
    resolver = SenseResolver()
    semantic = SimpleNamespace(
        domains=["weather"],
        concepts=["forecast"],
        search_intent="current weather conditions in the Philippines",
    )

    time_match = {
        "domain": "time",
        "concept": "present_state",
        "matched": "current",
        "confidence": 1.0,
    }
    electrical_match = {
        "domain": "engineering",
        "concept": "electrical",
        "matched": "current",
        "confidence": 1.0,
    }

    resolved_time = resolver.adjust(time_match, semantic, "current weather")
    resolved_electrical = resolver.adjust(
        electrical_match,
        semantic,
        "current weather",
    )

    assert resolved_time["confidence"] > resolved_electrical["confidence"]


def test_current_prefers_electrical_sense_for_electrical_intent():
    resolver = SenseResolver()
    semantic = SimpleNamespace(
        domains=["engineering"],
        concepts=["electrical"],
        search_intent="calculate electrical current through a resistor",
    )

    time_match = {
        "domain": "time",
        "concept": "present_state",
        "matched": "current",
        "confidence": 1.0,
    }
    electrical_match = {
        "domain": "engineering",
        "concept": "electrical",
        "matched": "current",
        "confidence": 1.0,
    }

    resolved_time = resolver.adjust(time_match, semantic, "current resistor")
    resolved_electrical = resolver.adjust(
        electrical_match,
        semantic,
        "current resistor",
    )

    assert resolved_electrical["confidence"] > resolved_time["confidence"]


def test_ambiguous_current_without_intent_is_not_forced_to_one_domain():
    resolver = SenseResolver()
    semantic = SimpleNamespace(domains=[], concepts=[], search_intent="")

    match = {
        "domain": "engineering",
        "concept": "electrical",
        "matched": "current",
        "confidence": 1.0,
    }

    resolved = resolver.adjust(match, semantic, "current")

    assert resolved["confidence"] == 1.0
    assert resolved["sense_resolved"] is False
