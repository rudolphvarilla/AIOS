from types import SimpleNamespace

from core.search.semantic_loop import SemanticSearchManager


class FakeService:
    def __init__(self):
        self.queries = []

    def search(self, query):
        self.queries.append(query)
        return [SimpleNamespace(title="result", snippet="evidence", url="https://example.test")]


class FakePipeline:
    def __init__(self):
        self.calls = 0

    def process(self, query, results, fivewh=None):
        self.calls += 1
        accepted = self.calls >= 2
        context = SimpleNamespace(
            evaluation=SimpleNamespace(
                should_retry=not accepted,
                fivewh_missing=[] if accepted else ["where"],
                answerability_missing=[] if accepted else ["answer-bearing data"],
                reason="accepted" if accepted else "missing evidence",
            )
        )
        return results, object(), "summary", context


def test_manager_rebuilds_search_after_judge_failure():
    service = FakeService()
    pipeline = FakePipeline()
    fivewh = SimpleNamespace(
        what="weather",
        when="current",
        where="Manila",
        how="conditions",
    )

    results, knowledge, summary, context, attempts = SemanticSearchManager().run(
        original_query="current weather in Manila",
        semantic_query="current weather Manila",
        fivewh=fivewh,
        service=service,
        pipeline=pipeline,
        max_retries=2,
    )

    assert pipeline.calls == 2
    assert len(service.queries) == 2
    assert service.queries[0] == "current weather Manila"
    assert "missing evidence" in service.queries[1]
    assert "where" in service.queries[1]
    assert context.evaluation.should_retry is False
    assert attempts[-1]["accepted"] is True
    assert results
    assert knowledge is not None
    assert summary == "summary"
