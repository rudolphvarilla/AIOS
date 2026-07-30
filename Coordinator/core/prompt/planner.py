"""
===========================================================
AIOS Prompt Planner
core/prompt/planner.py
===========================================================

Determines which prompt blocks should be included for the
current request.

The planner never builds prompts.

It only selects which blocks are required.

Version 4

Prompt Planner reads only from ExecutionPlan and DecisionEngine.

ExecutionPlan determines AIOS behavior.

Prompt Planner simply translates that plan into enabled
Prompt Blocks.
===========================================================
"""

from core.prompt.registry import PROMPT_BLOCKS


# ---------------------------------------------------------
# Prompt blocks that are ALWAYS required.
# These are never controlled by ExecutionPlan.
# ---------------------------------------------------------

MANDATORY_PROMPTS = [

    "user",

]


class PromptPlanner:

    def plan(self, state):

        # ---------------------------------
        # Initialize every prompt block OFF
        # ---------------------------------

        plan = {

            name: False

            for name in PROMPT_BLOCKS

        }

        # ---------------------------------
        # Safety
        # ---------------------------------

        if state.plan is None:

            # Mandatory blocks still apply

            for block in MANDATORY_PROMPTS:

                plan[block] = True

            return plan

        # ---------------------------------
        # Prompt blocks requested by planner
        # ---------------------------------

        plan.update(state.plan.prompt_flags)

        # ---------------------------------
        # Session Memory
        # ---------------------------------

        SESSION_MEMORY_TRIGGERS = [

            "previous",

            "last",

            "again",

            "continue",

        ]

        # ---------------------------------
        # Long-Term Memory
        # ---------------------------------

        LONGTERM_TRIGGERS = [

            "remember",

            "favorite",

            "my",

            "prefer",

            "usually",

        ]

        query = state.user_input.lower()

        if any(trigger in query for trigger in SESSION_MEMORY_TRIGGERS):

            plan["memory"] = True

        if any(trigger in query for trigger in LONGTERM_TRIGGERS):

            plan["longterm"] = True

        # ---------------------------------
        # Mandatory prompt blocks
        # ---------------------------------

        for block in MANDATORY_PROMPTS:

            plan[block] = True

        # ---------------------------------
        # Search comes from Decision Engine
        # ---------------------------------

        if state.decision is not None:

            plan["search"] = state.decision.use_search

        return plan