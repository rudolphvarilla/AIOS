from types import SimpleNamespace

from core.search.pipeline import SearchPipeline
from core.search.result import SearchResult
from core.search.semantic_loop import SemanticSearchManager
from core.services.search_service import SearchService


# Purpose: Provide the deterministic 5WH object required by the integration path.
# Inputs: None.
# Expected behavior: Return a complete semantic request description for current
# weather in Manila so the real service/pipeline path can be exercised without
# invoking an external semantic model.
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


# Purpose: Construct a SearchResult fixture with only the fields relevant to the
# integration tests.
# Inputs: title, snippet, and url strings representing one search result.
# Expected behavior: Return a SearchResult attributed to the deterministic
# integration-test source.
def result(title, snippet, url):
    return SearchResult(
        title=title,
        url=url,
        snippet=snippet,
        source="IntegrationTest",
    )


class FakeAggregator:
    """Deterministic provider boundary for the real SearchService facade."""

    # Purpose: Initialize the deterministic provider batches and call counter.
    # Inputs: batches, a sequence of result batches returned on successive calls.
    # Expected behavior: Preserve the supplied batches and start the provider
    # call count at zero.
    def __init__(self, batches):
        self.batches = list(batches)
        self.calls = 0

    # Purpose: Return the next deterministic provider batch while honoring the
    # SearchService result limit.
    # Inputs: query and max_results supplied by SearchService.
    # Expected behavior: Increment the call counter and return the corresponding
    # batch, repeating the final batch when the retry loop makes extra calls.
    def search(self, query, max_results=5):
        self.calls += 1
        batch = self.batches[min(self.calls - 1, len(self.batches) - 1)]
        return batch[:max_results]


# Purpose: Build the real SearchService facade around a deterministic provider.
# Inputs: batches, the provider responses that should be returned on each call.
# Expected behavior: Return a SearchService whose aggregator is isolated from
# external providers while retaining the production service boundary.
def build_service(batches):
    service = SearchService()
    service.aggregator = FakeAggregator(batches)
    return service


# Purpose: Verify that the semantic manager can retry through the real service
# and pipeline and return the validated second attempt.
# Inputs: A first landing-page result followed by answer-bearing Manila weather
# evidence.
# Expected behavior: The first attempt is rejected, the second is accepted, the
# service makes exactly two provider calls, and the validated context is returned.
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


# Purpose: Verify the exact retry-budget contract through the real service and
# pipeline rather than a mocked manager/pipeline boundary.
# Inputs: A permanently insufficient landing-page result and max_retries=2.
# Expected behavior: One initial attempt plus two retries produces exactly three
# provider calls, preserves all attempt records, and returns the best available
# unaccepted context without falsely marking the final attempt as stagnated.
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
