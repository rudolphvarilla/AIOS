"""
AIOS Executor
core/executor.py

Executes the execution plan created by the Planner.

Execution Pipeline

Decision Engine
        ↓
Services
        ↓
Search Pipeline
        ↓
Prompt Builder
        ↓
Selected Model
        ↓
Response

Version 1.2
"""

from core.services.manager import ServiceManager
from core.prompt.builder import PromptBuilder
from core.search.pipeline import SearchPipeline
from core.longterm.retrieval import LongTermRetrieval

from models.qwen3_4b import model as fast_general_model
from models.qwen3_8b import model as deep_reasoning_model
from models.qwen25coder import model as coding_model


service_manager = ServiceManager()
prompt_builder = PromptBuilder()
search_pipeline = SearchPipeline()
longterm_retrieval =LongTermRetrieval()

# --------------------------------------------------
# Search Retry Evaluation
# --------------------------------------------------

def should_retry_search(state):

    if state.search_context is None:
        return False

    if state.search_evaluation is None:
        return False

    evaluation = state.search_evaluation

    if not evaluation.should_retry:
        return False

    if state.search_retry_count >= state.max_search_retry:
        return False

    return True

def execute(state):

    # --------------------------------------------------
    # Developer Information
    # --------------------------------------------------

    if state.decision is not None:

        print("\nDecision received by Executor.")

        print(f"Use Search : {state.decision.use_search}")
        print(f"Background : {state.decision.background}")
        print(f"Reason     : {state.decision.reasoning}")

    # --------------------------------------------------
    # Service Execution
    # --------------------------------------------------

    if (
        state.decision is not None
        and
        state.decision.use_search
    ):

        service = service_manager.select("SEARCH")

        if service is not None:

            while True:

                search_query = state.user_input

                if (
                    getattr(state, "semantic", None)
                    and getattr(state.semantic, "search_query", "")
                ):
                    search_query = state.semantic.search_query

                raw_results = service.search(
                    query=search_query,
                )

                if not raw_results:
                    state.search_results = []
                    state.search_knowledge = None
                    state.search_summary = None
                    state.search_context = None
                    state.search_evaluation = None
                    state.search_retry = False
                    break

                (
                    state.search_results,
                    state.search_knowledge,
                    state.search_summary,
                    state.search_context,
                ) = search_pipeline.process(
                    query=search_query,
                    results=raw_results,
                )

                state.search_evaluation = state.search_context.evaluation

                state.search_retry = should_retry_search(state)

                evaluation = state.search_evaluation

                print("\n===== SEARCH EVALUATION =====")
                print(f"Confidence       : {evaluation.confidence:.2f}")
                print(f"Entities         : {evaluation.entity_count}")
                print(f"Recommendations  : {evaluation.recommendation_count}")
                print(f"Facts            : {evaluation.fact_count}")
                print(f"Retry            : {evaluation.should_retry}")
                print(f"Reason           : {evaluation.reason}")

                print(
                    f"Retry Count      : "
                    f"{state.search_retry_count}/{state.max_search_retry}"
                )

                if not state.search_retry:

                    break

                print("\nRetrying search...")

                state.search_retry_count += 1

                # ---------------------------------------------
                # Search Evaluation
                # ---------------------------------------------

                state.search_evaluation = state.search_context.evaluation

                state.search_retry = should_retry_search(state)

                evaluation = state.search_evaluation

                print("\n===== SEARCH EVALUATION =====")

                print(f"Confidence       : {evaluation.confidence:.2f}")
                print(f"Entities         : {evaluation.entity_count}")
                print(f"Recommendations  : {evaluation.recommendation_count}")
                print(f"Facts            : {evaluation.fact_count}")

                print(f"Retry            : {evaluation.should_retry}")
                print(f"Reason           : {evaluation.reason}")

                print(
                    f"Retry Count      : "
                    f"{state.search_retry_count}/{state.max_search_retry}"
                )

            else:

                state.search_results = []
                state.search_knowledge = None
                state.search_summary = None
                state.search_context = None
                state.search_evaluation = None
                state.search_retry = False

    # --------------------------------------------------
    # Long-Term Memory Retrieval
    # --------------------------------------------------

    state.longterm_memories = longterm_retrieval.retrieve(
        query = state.user_input,
        limit=5,
    )

    if state.longterm_memories:

        print(f"\nLong-Term Memories Retrieved : {len(state.longterm_memories)}")

        for memory in state.longterm_memories:

            print(f"  • {memory.title}")

    else:

        print("\nLong-Term Memories Retrieved : 0")

    # --------------------------------------------------
    # Build Prompt
    # --------------------------------------------------

    state.prompt = prompt_builder.build(state)

    # --------------------------------------------------
    # Developer Simulation Mode
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Execute Selected Model
    # --------------------------------------------------

    if state.selected_model == "qwen3:4b":

        state.response = fast_general_model.ask(

            state.prompt

        )

    elif state.selected_model == "qwen3:8b":

        state.response = deep_reasoning_model.ask(

            state.prompt

        )

    elif state.selected_model == "qwen2.5-coder:3b":

        state.response = coding_model.ask(

            state.prompt

        )

    else:

        state.response = (

            f"Unknown model: {state.selected_model}"

        )

    return state