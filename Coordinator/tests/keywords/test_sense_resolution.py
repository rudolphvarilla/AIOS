from types import SimpleNamespace

from core.keywords.matcher import KeywordMatcher


def test_current_weather_resolves_to_temporal_time_domain():
    semantic = SimpleNamespace(
        domains=["weather"],
        concepts=["forecast"],
        search_intent="current weather conditions in the Philippines",
    )

    matches = KeywordMatcher().match(
        "current weather in Philippines",
        semantic=semantic,
    )

    current_matches = [
        item for item in matches
        if item["matched"].casefold() == "current"
    ]

    assert current_matches
    assert current_matches[0]["domain"] == "time"
    assert current_matches[0]["concept"] == "present_state"


def test_current_electrical_resolves_to_engineering_domain():
    semantic = SimpleNamespace(
        domains=["engineering"],
        concepts=["electrical"],
        search_intent="calculate electrical current through a resistor",
    )

    matches = KeywordMatcher().match(
        "current through a resistor",
        semantic=semantic,
    )

    current_matches = [
        item for item in matches
        if item["matched"].casefold() == "current"
    ]

    assert current_matches
    assert current_matches[0]["domain"] == "engineering"
    assert current_matches[0]["concept"] == "electrical"


def test_bare_current_keeps_competing_senses():
    semantic = SimpleNamespace(
        domains=[],
        concepts=[],
        search_intent="",
    )

    matches = KeywordMatcher().match("current", semantic=semantic)

    current_matches = [
        item for item in matches
        if item["matched"].casefold() == "current"
    ]

    domains = {item["domain"] for item in current_matches}
    assert "time" in domains
    assert "engineering" in domains
