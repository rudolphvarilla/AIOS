"""
AIOS Executor
core/executor.py

Executes the execution plan created by the Planner.

Version 1.4 - Phase 3.1.16 Builder/Judge/Manager semantic search loop
"""

from core.services.manager import ServiceManager
from core.prompt.builder import PromptBuilder
from core.search.pipeline import SearchPipeline
from core.search.semantic_loop import SemanticSearchManager
from core.longterm.retrieval import LongTermRetrieval

from models.qwen3_4b import model as fast_general_model
from models.qwen3_8b import model as deep_reasoning_model
from models.qwen25coder import model as coding_model


service_manager = ServiceManager()
prompt_builder = PromptBuilder()
search_pipeline = SearchPipeline()
search_loop_manager = SemanticSearchManager()
longterm_retrieval = LongTermRetrieval()


def should_retry_search(state):
    if state.search_context is None:
        return False
    if state.search_evaluation is None:
        return False
    if not state.search_evaluation.should_retry:
        return False
    return state.search_retry_count < state.max_search_retry


def execute(state):

    if state.decision is not None:
        print("\nDecision received by Executor.")
        print(f"Use Search : {state.decision.use_search}")
        print(f"Background : {state.decision.background}")
        print(f"Reason     : {state.decision.reasoning}")

    if state.decision is not None and state.decision.use_search:
        service = service_manager.select("SEARCH")

        if service is not None:
            semantic_query = ""
            if getattr(state, "semantic", None):
                semantic_query = getattr(state.semantic, "search_query", "") or ""

            (
                state.search_results,
                state.search_knowledge,
                state.search_summary,
                state.search_context,
                state.search_loop_attempts,
            ) = search_loop_manager.run(
                original_query=state.user_input,
                semantic_query=semantic_query,
                fivewh=getattr(state, "fivewh", None),
                service=service,
                pipeline=search_pipeline,
                max_retries=state.max_search_retry,
            )

            state.search_retry_count = max(0, len(state.search_loop_attempts or []) - 1)
            state.search_evaluation = (
                state.search_context.evaluation if state.search_context is not None else None
            )
            state.search_retry = should_retry_search(state)
            state.search_loop_accepted = bool(
                state.search_loop_attempts
                and state.search_loop_attempts[-1].get("accepted", False)
            )
            state.search_feedback = (
                state.search_loop_attempts[-1].get("feedback", [])
                if state.search_loop_attempts else []
            )

            print("\n===== SEMANTIC SEARCH LOOP =====")
            for attempt in state.search_loop_attempts or []:
                evaluation = attempt.get("evaluation")
                print(f"Attempt          : {attempt.get('attempt', 0)}")
                print(f"Builder Query    : {attempt['build'].query}")
                print(f"Accepted         : {attempt.get('accepted', False)}")
                if evaluation is not None:
                    print(f"Judge Confidence : {evaluation.confidence:.2f}")
                    print(f"Judge Reason     : {evaluation.reason}")
                if attempt.get("feedback"):
                    print(f"Judge Feedback   : {attempt['feedback']}")

            if state.search_context is None:
                state.search_results = []
                state.search_knowledge = None
                state.search_summary = None
                state.search_evaluation = None
                state.search_retry = False
                state.search_loop_accepted = False

    else:
        state.search_results = []
        state.search_knowledge = None
        state.search_summary = None
        state.search_context = None
        state.search_evaluation = None
        state.search_retry = False
        state.search_loop_attempts = []
        state.search_feedback = []
        state.search_loop_accepted = False

    state.longterm_memories = longterm_retrieval.retrieve(
        query=state.user_input,
        limit=5,
    )

    if state.longterm_memories:
        print(f"\nLong-Term Memories Retrieved : {len(state.longterm_memories)}")
        for memory in state.longterm_memories:
            print(f"  • {memory.title}")
    else:
        print("\nLong-Term Memories Retrieved : 0")

    # The Manager/Judge gate is deliberately before the LLM. If search was
    # requested but deterministic validation exhausted its retry budget, fail
    # closed instead of asking the LLM to manufacture an answer from weak
    # evidence.
    if state.decision is not None and state.decision.use_search and not state.search_loop_accepted:
        state.response = (
            "I could not obtain enough validated search evidence to answer this "
            "reliably. The search manager exhausted its retry budget.\n\n"
            f"Judge feedback: {', '.join(state.search_feedback) or 'insufficient evidence'}"
        )
        return state

    state.prompt = prompt_builder.build(state)

    if state.simulation:
        state.response = (
            "[SIMULATION MODE]\n\n"
            f"Model            : {state.selected_model}\n"
            f"Model Capability : {state.plan.model_capability}\n"
            f"Tool Capability  : {state.plan.tool_capability}\n"
            f"Complexity       : {state.plan.complexity}\n"
            f"Use Search       : {state.decision.use_search if state.decision else False}\n"
            f"Search Results   : {len(state.search_results) if state.search_results else 0}\n\n"
            "All infrastructure executed successfully.\n"
            "LLM inference skipped.\n\n"
            "Turn Simulation Mode OFF\n"
            "/dev sim off\n"
            "to execute the selected model."
        )
        return state

    if state.selected_model == "qwen3:4b":
        state.response = fast_general_model.ask(state.prompt)
    elif state.selected_model == "qwen3:8b":
        state.response = deep_reasoning_model.ask(state.prompt)
    elif state.selected_model == "qwen2.5-coder:3b":
        state.response = coding_model.ask(state.prompt)
    else:
        state.response = f"Unknown model: {state.selected_model}"

    return state
