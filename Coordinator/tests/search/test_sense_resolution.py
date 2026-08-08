from types import SimpleNamespace

from core.context.engine import ContextEngine


def test_current_resolves_to_time_for_weather_intent():
    result = ContextEngine().analyze("current weather in Philippines")

    assert "time" in result.concepts
    assert "temporal_now" in result.concepts["time"]
    assert result.primary_domain != "engineering"

    current_matches = [
        item for item in result.matches
        if item.get("matched") == "current"
    ]
    assert current_matches
    assert all(item.get("sense") == "temporal" for item in current_matches)


def test_current_resolves_to_electrical_for_circuit_intent():
    result = ContextEngine().analyze("current voltage and resistance in a circuit")

    assert "engineering" in result.concepts
    assert "electrical" in result.concepts["engineering"]

    current_matches = [
        item for item in result.matches
        if item.get("matched") == "current"
    ]
    assert current_matches
    assert all(item.get("sense") == "electrical" for item in current_matches)


def test_semantic_domain_can_break_an_ambiguous_tie():
    semantic = SimpleNamespace(
        domains=["time"],
        concepts=["temporal_now"],
    )

    result = ContextEngine().analyze("current", semantic=semantic)

    current_matches = [
        item for item in result.matches
        if item.get("matched") == "current"
    ]
    assert current_matches
    assert all(item.get("sense") == "temporal" for item in current_matches)
