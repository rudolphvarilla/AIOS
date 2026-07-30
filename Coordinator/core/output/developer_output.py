"""
===========================================================
AIOS Developer Output
core/output/developer_output.py
===========================================================

Responsible for printing all developer mode diagnostics.

core/output/presenter.py should only call:

DeveloperOutput().present(state, memory, scheduler, perf)

===========================================================
"""

from core.config import (
    PROMPT_PREVIEW_LIMIT,
    TOKEN_ESTIMATE_DIVISOR,
)


class DeveloperOutput:

    def present(self, state, memory, scheduler, perf):

        # Routing
        self.routing(state)
 
        # Prompt
        self.prompt(state)

        # Execution Plan
        self.execution_plan(state)

        # Context
        self.context(state)

        # Perception
        self.perception(state)

        # Working Memory
        self.working_memory(memory)

        # Session Memory
        self.session_memory(memory)

        # Background
        self.background_queue(scheduler)

        # Performance
        perf.report()

    # =====================================================
    # Routing

    def routing(self, state):

        print("\n===== ROUTING RESULT =====")

        print(f"Simulation       : {'ON' if state.simulation else 'OFF'}")
        print(f"Intent           : {state.intent_result.intent}")
        print(f"Confidence       : {state.intent_result.confidence:.2f}")
        print(f"Capability       : {state.intent_result.capability}")
        print(f"Reason           : {state.intent_result.reasoning}")
        print(f"Complexity       : {state.plan.complexity}")
        print(f"Model            : {state.selected_model}")
        print(f"Model Capability : {state.plan.model_capability}")
        print(f"Tool Capability  : {state.plan.tool_capability}")
        print(f"Browser           : {state.plan.browser}")
        print(f"Vision            : {state.plan.vision}")
        print(f"Image Generation  : {state.plan.image_generation}")
        print(f"Use Search       : {state.decision.use_search}")
        print(f"Background       : {state.decision.background}")
        print(f"Decision         : {state.decision.reasoning}")

        if state.search_results:
            print(f"Search Results   : {len(state.search_results)}")

    # =====================================================
    # Prompt

    def prompt(self, state):

        if not state.prompt:
            return

        print("\n===== PROMPT PLANNER =====")

        for name, enabled in state.prompt_plan.items():

            print(f"{name:<12}: {'ON' if enabled else 'OFF'}")

        print("\n===== PROMPT INSPECTOR =====")

        prompt_length = len(state.prompt)

        estimated_tokens = prompt_length // TOKEN_ESTIMATE_DIVISOR

        print(f"Prompt Length   : {prompt_length} characters")
        print(f"Estimated Tokens: ~{estimated_tokens}")

        print("\n===== PROMPT PREVIEW =====")

        preview = state.prompt[:PROMPT_PREVIEW_LIMIT]

        print(f"Preview Limit : {PROMPT_PREVIEW_LIMIT}")

        print(preview)

        if prompt_length > PROMPT_PREVIEW_LIMIT:

            print("\n... (truncated)")

    # =====================================================
    # Execution Plan

    def execution_plan(self, state):

        print("\n===== EXECUTION PLAN =====")

        print(f"Model Capability  : {state.plan.model_capability}")
        print(f"Tool Capability   : {state.plan.tool_capability}")

    # =====================================================
    # Context

    def context(self, state):

        print("\n===== CONTEXT ENGINE =====")

        print(f"Primary Domain  : {state.context.primary_domain}")
        print(f"Primary Concept : {state.context.primary_concept}")

        print("\nDomain Scores")

        for domain, score in state.context.domain_scores.items():

            print(f"  {domain:<15} {score}")

        print("\nConcept Scores")

        for domain, concepts in state.context.concept_scores.items():

            print(domain)

            for concept, score in concepts.items():

                print(f"    {concept:<20} {score}")

        print("\nMatches")

        for item in state.context.matches:

            print(item)

    # =====================================================
    # Perception

    def perception(self, state):

        if state.perception is None:
            return

        print("\n===== PERCEPTION =====")

        print(state.perception)

    # =====================================================
    # Working Memory

    def working_memory(self, memory):

        print("\n===== WORKING MEMORY =====")

        print(memory.working)

    # =====================================================
    # Session Memory

    def session_memory(self, memory):

        print("\n===== SESSION MEMORY =====")

        history = memory.session.history

        print(f"Entries : {len(history)}")

        for item in history[-3:]:

            print(item)

    # =====================================================
    # Background

    def background_queue(self, scheduler):

        print("\n===== BACKGROUND QUEUE =====")

        jobs = scheduler.queue.list_jobs()

        print(f"Pending Jobs : {len(jobs)}")

        for i, job in enumerate(jobs[-3:], start=1):

            print()

            print(f"[{i}]")

            print(f"Status      : {job.status}")

            print(f"Description : {job.description}")

            print(f"Created     : {job.timestamp}")