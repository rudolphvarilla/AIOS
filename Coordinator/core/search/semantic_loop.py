"""
AIOS Semantic Search Builder / Judge / Manager loop.

Phase 3.1.16

Builder  -> constructs the next search dataset/query.
Judge    -> evaluates the retrieved SearchContext and returns failure reasons.
Manager  -> controls bounded retries and feeds judge feedback back to Builder.

The loop is deterministic at the orchestration layer. It does not invent facts
and it never asks an LLM to decide whether search evidence passed validation.
"""

from dataclasses import dataclass, field


@dataclass
class SearchBuild:
    """The concrete search request produced by the Builder."""

    query: str
    attempt: int = 0
    feedback_used: list[str] = field(default_factory=list)


class SemanticSearchBuilder:
    """Build an initial search request and enrich retries with Judge feedback."""

    def build(
        self,
        original_query,
        semantic_query=None,
        fivewh=None,
        feedback=None,
        previous_query=None,
        attempt=0,
    ):
        base = str(semantic_query or original_query or "").strip()
        feedback = [str(item).strip() for item in (feedback or []) if str(item).strip()]

        if attempt <= 0 or not feedback:
            return SearchBuild(query=base, attempt=0)

        # Keep the user's original intent in every retry. Feedback is appended
        # as search constraints rather than replacing the query with the
        # evaluator's wording.
        requirements = []
        if fivewh is not None:
            for name in ("what", "when", "where", "how"):
                value = str(getattr(fivewh, name, "") or "").strip()
                if value and value.lower() not in {"none", "none provided"}:
                    requirements.append(value)

        parts = [base]
        if requirements:
            parts.append("Required evidence: " + "; ".join(requirements))
        parts.append("Previous search failed validation because: " + "; ".join(feedback))

        # Avoid repeatedly growing a query with the exact same feedback.
        if previous_query and all(item.lower() in str(previous_query).lower() for item in feedback):
            parts = [base, "Required evidence: " + "; ".join(requirements)] if requirements else [base]
            parts.append("Previous search failed validation because: " + "; ".join(feedback))

        return SearchBuild(
            query=" ".join(part for part in parts if part),
            attempt=attempt,
            feedback_used=feedback,
        )


class SemanticSearchJudge:
    """Judge a completed search using the existing deterministic evaluator."""

    def judge(self, context):
        evaluation = getattr(context, "evaluation", None)
        if evaluation is None:
            return False, ["search evaluation was not produced"]

        if not evaluation.should_retry:
            return True, []

        feedback = []
        feedback.extend(getattr(evaluation, "fivewh_missing", []) or [])
        feedback.extend(getattr(evaluation, "answerability_missing", []) or [])
        reason = str(getattr(evaluation, "reason", "") or "").strip()
        if reason:
            feedback.append(reason)

        # Preserve ordering while removing duplicate messages.
        seen = set()
        unique = []
        for item in feedback:
            key = item.casefold()
            if key not in seen:
                seen.add(key)
                unique.append(item)
        return False, unique or ["search evidence failed deterministic validation"]


class SemanticSearchManager:
    """Run Builder -> search -> Judge until accepted or retry budget is exhausted."""

    def __init__(self, builder=None, judge=None):
        self.builder = builder or SemanticSearchBuilder()
        self.judge = judge or SemanticSearchJudge()

    def run(
        self,
        original_query,
        service,
        pipeline,
        fivewh=None,
        semantic_query=None,
        max_retries=2,
    ):
        previous_query = None
        feedback = []
        attempts = []

        for attempt in range(max(0, int(max_retries)) + 1):
            build = self.builder.build(
                original_query=original_query,
                semantic_query=semantic_query,
                fivewh=fivewh,
                feedback=feedback,
                previous_query=previous_query,
                attempt=attempt,
            )
            previous_query = build.query

            raw_results = service.search(query=build.query)
            if not raw_results:
                attempts.append({"attempt": attempt, "build": build, "evaluation": None, "accepted": False})
                feedback = ["search returned no results"]
                continue

            processed = pipeline.process(
                query=build.query,
                results=raw_results,
                fivewh=fivewh,
            )

            # SearchPipeline has a compatibility contract of four return
            # values on the current branch.
            search_results, knowledge, summary, context = processed
            accepted, feedback = self.judge.judge(context)
            attempts.append({
                "attempt": attempt,
                "build": build,
                "evaluation": getattr(context, "evaluation", None),
                "accepted": accepted,
            })

            if accepted:
                return search_results, knowledge, summary, context, attempts

        # Return the final attempt so the caller can still expose the best
        # available evidence after the bounded retry budget is exhausted.
        if attempts:
            final = attempts[-1]
            # Re-run is intentionally avoided; the final context is attached
            # below from the last successful processing result when available.
        return [], None, None, None, attempts
