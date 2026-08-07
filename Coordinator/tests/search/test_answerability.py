from types import SimpleNamespace

from core.search.answerability import AnswerabilityValidator
from core.search.evaluator import SearchEvaluator
from core.search.context import SearchContext


validator = AnswerabilityValidator()


def fivewh(**values):
    defaults = {
        "who": "user",
        "what": "weather",
        "when": "current",
        "where": "Philippines",
        "why": "information",
        "how": "none provided",
        "confidence": 1.0,
    }
    defaults.update(values)
    return SimpleNamespace(**defaults)


def result(title, snippet):
    return SimpleNamespace(
        title=title,
        snippet=snippet,
        url="https://example.com/weather",
    )


def test_current_weather_landing_pages_are_not_answerable():
    results = [
        result(
            "Philippines Current Weather | AccuWeather",
            "Get the Philippines weather forecast including current conditions across major cities.",
        ),
        result(
            "BBC Weather - Home",
            "Latest weather conditions and forecasts for the UK and the world.",
        ),
    ]

    evaluation = validator.validate(
        fivewh(),
        results,
        summary="Philippines weather forecast and current conditions.",
    )

    assert evaluation.slot_scores["topic_evidence"] == 1.0
    assert evaluation.slot_scores["location_evidence"] == 1.0
    assert evaluation.slot_scores["time_evidence"] == 1.0
    assert evaluation.slot_scores["answer_data"] == 0.0
    assert "answer-bearing data" in evaluation.missing


def test_current_weather_with_numeric_conditions_is_answerable():
    evaluation = validator.validate(
        fivewh(),
        [
            result(
                "Manila Current Weather",
                "Current conditions in Manila, Philippines: 28°C, humidity 82%, winds 18 km/h, 60% chance of rain.",
            )
        ],
        summary="Current weather conditions for Manila, Philippines.",
    )

    assert evaluation.score == 1.0
    assert evaluation.missing == []


def test_current_weather_with_explicit_condition_is_answerable():
    evaluation = validator.validate(
        fivewh(),
        [
            result(
                "Manila Weather Now",
                "Currently in Manila, Philippines: cloudy with occasional showers and local thunderstorms.",
            )
        ],
        summary="Current weather conditions in Manila, Philippines.",
    )

    assert evaluation.slot_scores["answer_data"] == 1.0
    assert evaluation.missing == []


def test_future_weather_forecast_can_be_answerable_without_current_observation():
    request = fivewh(
        when="September 2026",
        where="Tokyo",
    )

    evaluation = validator.validate(
        request,
        [
            result(
                "Tokyo September 2026 Weather Forecast",
                "Tokyo September 2026 weather forecast and outlook, including expected temperatures and rainfall patterns.",
            )
        ],
        summary="Tokyo September 2026 weather forecast and outlook.",
    )

    assert evaluation.slot_scores["time_evidence"] == 1.0
    assert evaluation.slot_scores["answer_data"] == 1.0
    assert evaluation.missing == []


def test_wrong_location_fails_answerability():
    request = fivewh(where="Tokyo")

    evaluation = validator.validate(
        request,
        [
            result(
                "Manila Current Weather",
                "Current conditions in Manila, Philippines: 28°C and cloudy.",
            )
        ],
        summary="Current weather in Manila, Philippines.",
    )

    assert evaluation.slot_scores["location_evidence"] == 0.0
    assert "location evidence" in evaluation.missing


def test_missing_time_evidence_fails_future_request():
    request = fivewh(
        when="September 2026",
        where="Tokyo",
    )

    evaluation = validator.validate(
        request,
        [
            result(
                "Tokyo Weather Forecast",
                "Tokyo weather forecast with expected temperatures and rainfall patterns.",
            )
        ],
        summary="Tokyo weather forecast.",
    )

    assert evaluation.slot_scores["time_evidence"] == 0.0
    assert "time evidence" in evaluation.missing


def test_generic_short_evidence_is_not_answerable():
    request = fivewh(what="history", when="none provided", where="France")

    evaluation = validator.validate(
        request,
        [result("France", "France")],
        summary="France",
    )

    assert evaluation.score < 0.60
    assert "answer-bearing data" in evaluation.missing


def test_search_evaluator_retries_when_answerability_is_low():
    context = SearchContext(
        topic="current weather in the Philippines",
        summary="Philippines current weather forecast.",
        entities=["Philippines"],
        confidence=0.95,
    )
    context.fivewh_alignment = SimpleNamespace(
        score=1.0,
        missing=[],
    )
    context.answerability = SimpleNamespace(
        score=0.20,
        missing=["answer-bearing data"],
    )

    evaluation = SearchEvaluator().evaluate_context(context)

    assert evaluation.confidence < 0.70
    assert evaluation.answerability_score == 0.20
    assert evaluation.should_retry is True
    assert "answer-bearing evidence" in evaluation.reason
