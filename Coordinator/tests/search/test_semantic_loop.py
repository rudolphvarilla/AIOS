from types import SimpleNamespace

from core.search.semantic_loop import SemanticSearchBuilder, SemanticSearchJudge


def test_builder_keeps_original_query_and_injects_judge_feedback():
    fivewh = SimpleNamespace(
        what="weather",
        when="current",
        where="Manila",
        how="conditions",
    )

    build = SemanticSearchBuilder().build(
        original_query="current weather in Manila",
        semantic_query="current weather Manila",
        fivewh=fivewh,
        feedback=["answer-bearing data", "time evidence"],
        attempt=1,
    )

    assert "current weather Manila" in build.query
    assert "Required evidence: weather; current; Manila; conditions" in build.query
    assert "answer-bearing data" in build.query
    assert "time evidence" in build.query
    assert build.attempt == 1


def test_judge_accepts_context_when_evaluator_passes():
    context = SimpleNamespace(
        evaluation=SimpleNamespace(should_retry=False, reason="accepted")
    )

    accepted, feedback = SemanticSearchJudge().judge(context)

    assert accepted is True
    assert feedback == []


def test_judge_returns_structured_retry_feedback():
    context = SimpleNamespace(
        evaluation=SimpleNamespace(
            should_retry=True,
            fivewh_missing=["where"],
            answerability_missing=["answer-bearing data"],
            reason="Insufficient answer-bearing evidence",
        )
    )

    accepted, feedback = SemanticSearchJudge().judge(context)

    assert accepted is False
    assert feedback == [
        "where",
        "answer-bearing data",
        "Insufficient answer-bearing evidence",
    ]
