"""
AIOS Semantic Search Builder / Judge / Manager loop.

Phase 3.1.17

Builder  -> constructs the next search dataset/query.
Judge    -> determines whether the retrieved evidence passes.
Manager  -> feeds Judge feedback back into Builder and controls retries.

The orchestration layer is deterministic. It does not invent facts and does
not ask an LLM to decide whether the evidence passed the deterministic gate.
"""

from dataclasses import dataclass, field


@dataclass
class SearchBuild:
    query: str
    attempt: int = 0
    feedback_used: list[str] = field(default_factory=list)


class SemanticSearchBuilder:
    """Build the initial search request and feedback-enriched retries."""

    def build(self, original_query, semantic_query=None, fivewh=None,
              feedback=None, previous_query=None, attempt=0):
        base = str(semantic_query or original_query or "").strip()
        feedback = [str(item).strip() for item in (feedback or []) if str(item).strip()]

        if attempt <= 0 or not feedback:
            return SearchBuild(query=base, attempt=0)

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

        return SearchBuild(
            query=" ".join(part for part in parts if part),
            attempt=attempt,
            feedback_used=feedback,
        )


class SemanticSearchJudge:
    """Adapt the existing deterministic SearchEvaluation into loop feedback."""

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

    @staticmethod
    def _query_key(query):
        """Normalize a query for deterministic stagnation detection."""
        return " ".join(str(query or "").casefold().split())

    def run(self, original_query, service, pipeline, fivewh=None,
            semantic_query=None, max_retries=2):
        feedback = []
        attempts = []
        last_success = None
        previous_query_key = None

        for attempt in range(max(0, int(max_retries)) + 1):
            build = self.builder.build(
                original_query=original_query,
                semantic_query=semantic_query,
                fivewh=fivewh,
                feedback=feedback,
                previous_query=(
                    attempts[-1]["build"].query if attempts else None
                ),
                attempt=attempt,
            )

            query_key = self._query_key(build.query)
            # A repeated query is only a stagnation condition when the Builder
            # did not incorporate any Judge feedback. A feedback-enriched build
            # is a deliberate retry even if the resulting query text happens to
            # normalize to the same value as the preceding enriched build.
            feedback_used = getattr(build, "feedback_used", []) or []
            if attempt > 0 and query_key == previous_query_key and not feedback_used:
                feedback = [
                    "builder produced no new search query after judge feedback"
                ]
                attempts.append({
                    "attempt": attempt,
                    "build": build,
                    "evaluation": (
                        getattr(last_success[3], "evaluation", None)
                        if last_success is not None else None
                    ),
                    "accepted": False,
                    "feedback": list(feedback),
                    "stagnated": True,
                })
                break

            previous_query_key = query_key

            raw_results = service.search(query=build.query)
            if not raw_results:
                attempts.append({
                    "attempt": attempt,
                    "build": build,
                    "evaluation": None,
                    "accepted": False,
                    "feedback": ["search returned no results"],
                    "stagnated": False,
                })
                feedback = ["search returned no results"]
                continue

            search_results, knowledge, summary, context = pipeline.process(
                query=build.query,
                results=raw_results,
                fivewh=fivewh,
            )
            last_success = (search_results, knowledge, summary, context)
            accepted, feedback = self.judge.judge(context)
            attempts.append({
                "attempt": attempt,
                "build": build,
                "evaluation": getattr(context, "evaluation", None),
                "accepted": accepted,
                "feedback": list(feedback),
                "stagnated": False,
            })

            if accepted:
                return *last_success, attempts

        if last_success is not None:
            return *last_success, attempts
        return [], None, None, None, attempts
