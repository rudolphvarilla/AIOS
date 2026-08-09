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


MANDATORY_PROMPTS = ["user"]


class PromptPlanner:

    def plan(self, state):
        plan = {name: False for name in PROMPT_BLOCKS}

        execution_plan = getattr(state, "plan", None)
        if execution_plan is None:
            for block in MANDATORY_PROMPTS:
                plan[block] = True
            return plan

        plan.update(execution_plan.prompt_flags)

        session_memory_triggers = ["previous", "last", "again", "continue"]
        longterm_triggers = ["remember", "favorite", "my", "prefer", "usually"]

        query = getattr(state, "user_input", "").lower()

        if any(trigger in query for trigger in session_memory_triggers):
            plan["memory"] = True

        if any(trigger in query for trigger in longterm_triggers):
            plan["longterm"] = True

        for block in MANDATORY_PROMPTS:
            plan[block] = True

        decision = getattr(state, "decision", None)
        if decision is not None:
            plan["search"] = decision.use_search

        return plan
