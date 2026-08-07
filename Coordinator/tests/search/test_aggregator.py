"""Tests for multi-provider search aggregation."""

from dataclasses import dataclass

from core.search.aggregator import SearchAggregator
from core.search.result import SearchResult


@dataclass
class FakeProvider:
    results: list
    fail: bool = False

    def execute(self, query, max_results=5):
        if self.fail:
            raise RuntimeError("provider failure")
        return self.results[:max_results]


class FakeManager:
    def __init__(self, providers):
        self.providers = providers

    def select_all(self, service):
        assert service == "SEARCH"
        return self.providers


def result(title, url, source):
    return SearchResult(
        title=title,
        url=url,
        snippet=title,
        source=source,
    )


def test_aggregates_multiple_providers_and_deduplicates_urls():
    first = FakeProvider([
        result("A", "https://example.com/a", "Provider A"),
        result("Shared A", "https://example.com/shared", "Provider A"),
    ])
    second = FakeProvider([
        result("Shared B", "https://example.com/shared", "Provider B"),
        result("B", "https://example.com/b", "Provider B"),
    ])

    aggregator = SearchAggregator(FakeManager([first, second]))

    results = aggregator.search("test", max_results=5)

    assert [item.title for item in results] == ["A", "Shared A", "B"]
    assert [item.source for item in results] == [
        "Provider A",
        "Provider A",
        "Provider B",
    ]


def test_provider_failure_does_not_abort_aggregation():
    working = FakeProvider([
        result("Working", "https://example.com/working", "Working")
    ])
    failing = FakeProvider([], fail=True)

    aggregator = SearchAggregator(FakeManager([failing, working]))

    results = aggregator.search("test")

    assert len(results) == 1
    assert results[0].title == "Working"


def test_global_result_limit_is_enforced():
    first = FakeProvider([
        result("A", "https://example.com/a", "A"),
        result("B", "https://example.com/b", "A"),
    ])
    second = FakeProvider([
        result("C", "https://example.com/c", "B"),
        result("D", "https://example.com/d", "B"),
    ])

    aggregator = SearchAggregator(FakeManager([first, second]))

    results = aggregator.search("test", max_results=3)

    assert len(results) == 3
