from types import SimpleNamespace

from core.search.pipeline import SearchPipeline
from core.search.result import SearchResult
from core.search.semantic_loop import SemanticSearchManager
from core.services.search_service import SearchService


def fivewh():
    return SimpleNamespace(
        who="user",
        what="weather",
        when="current",
        where="Manila",
        why="information",
        how="none provided",
        confidence=1.0,
    )


def result(title, snippet, url):
    return SearchResult(
        title=title,
        url=url,
        snippet=snippet,
        source="IntegrationTest",
    )


class FakeAggregator:
    """Deterministic provider boundary for the real SearchService facade."""

    def __init__(self, batches):
        self.batches = list(batches)
        self.calls = 0

    def search(self, query, max_results=5):
        self.calls += 1
        batch = self.batches[min(self.calls - 1, len(self.batches) - 1)]
        return batch[:max_results]


def build_service(batches):
    service = SearchService()
    service.aggregator = FakeAggregator(batches)
    return service


def test_manager_retries_through_real_service_and_pipeline_then_returns_validated_context():
    service = build_service([
        [
            result(
                "Philippines Current Weather",
                "Get the Philippines weather forecast including current conditions across major cities.",
                "https://example.test/weather-landing",
            )
        ],
        [
            result(
                "Manila Current Weather",
                "Current conditions in Manila, Philippines: 28°C, humidity 82%, winds 18 km/h, 60% chance of rain.",
                "https://example.test/manila-weather",
            )
        ],
    ])

    results, knowledge, summary, context, attempts = SemanticSearchManager().run(
        original_query="current weather in Manila",
        semantic_query="current weather Manila",
        fivewh=fivewh(),
        service=service,
        pipeline=SearchPipeline(),
        max_retries=2,
    )

    assert service.aggregator.calls == 2
    assert len(attempts) == 2
    assert attempts[0]["accepted"] is False
    assert attempts[1]["accepted"] is True
    assert context.evaluation.should_retry is False
    assert context.answerability.missing == []
    assert summary == context.summary
    assert results
    assert knowledge is not None


def test_manager_uses_exact_retry_budget_with_real_service_and_pipeline():
    landing_page = result(
        "Philippines Current Weather",
        "Get the Philippines weather forecast including current conditions across major cities.",
        "https://example.test/weather-landing",
    )
    service = build_service([[landing_page]])

    results, knowledge, summary, context, attempts = SemanticSearchManager().run(
        original_query="current weather in Manila",
        semantic_query="current weather Manila",
        fivewh=fivewh(),
        service=service,
        pipeline=SearchPipeline(),
        max_retries=2,
    )

    assert service.aggregator.calls == 3
    assert len(attempts) == 3
    assert attempts[-1]["accepted"] is False
    assert attempts[-1]["stagnated"] is False
    assert context.evaluation.should_retry is True
    assert results
    assert knowledge is not None
    assert summary == context.summary
