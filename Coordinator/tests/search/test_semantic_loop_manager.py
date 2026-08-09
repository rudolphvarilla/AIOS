from types import SimpleNamespace

from core.search.semantic_loop import SemanticSearchManager


class FakeService:
    def __init__(self):
        self.queries = []

    def search(self, query):
        self.queries.append(query)
        return [SimpleNamespace(title="result", snippet="evidence", url="https://example.test")]


class FakePipeline:
    def __init__(self, pass_on=2):
        self.calls = 0
        self.pass_on = pass_on

    def process(self, query, results, fivewh=None):
        self.calls += 1
        accepted = self.calls >= self.pass_on
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
    pipeline = FakePipeline(pass_on=2)
    fivewh = SimpleNamespace(what="weather", when="current", where="Manila", how="conditions")

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
    assert attempts[-1]["stagnated"] is False
    assert results
    assert knowledge is not None
    assert summary == "summary"


def test_manager_returns_best_validated_attempt_when_retry_budget_exhausts():
    service = FakeService()
    pipeline = FakePipeline(pass_on=99)
    fivewh = SimpleNamespace(what="weather", when="current", where="Manila", how="conditions")

    results, knowledge, summary, context, attempts = SemanticSearchManager().run(
        original_query="current weather in Manila",
        semantic_query="current weather Manila",
        fivewh=fivewh,
        service=service,
        pipeline=pipeline,
        max_retries=2,
    )

    assert pipeline.calls == 3
    assert len(attempts) == 3
    assert attempts[-1]["accepted"] is False
    assert attempts[-1]["stagnated"] is False
    assert context is not None
    assert context.evaluation.should_retry is True
    assert results
    assert knowledge is not None
    assert summary == "summary"


def test_manager_stops_when_builder_repeats_same_query():
    service = FakeService()
    pipeline = FakePipeline(pass_on=99)

    class StagnantBuilder:
        def build(self, **kwargs):
            return SimpleNamespace(query="same query", attempt=kwargs.get("attempt", 0), feedback_used=[])

    results, knowledge, summary, context, attempts = SemanticSearchManager(
        builder=StagnantBuilder()
    ).run(
        original_query="original",
        semantic_query="same query",
        service=service,
        pipeline=pipeline,
        max_retries=5,
    )

    assert len(service.queries) == 1
    assert pipeline.calls == 1
    assert len(attempts) == 2
    assert attempts[-1]["accepted"] is False
    assert attempts[-1]["stagnated"] is True
    assert "no new search query" in attempts[-1]["feedback"][0]
    assert context.evaluation.should_retry is True
    assert results
    assert knowledge is not None
    assert summary == "summary"
