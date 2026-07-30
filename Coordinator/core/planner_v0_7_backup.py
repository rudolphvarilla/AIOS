"""
AIOS Execution Planner

Creates an execution plan based on the detected intent.

Future versions will use Qwen3 to generate these plans dynamically.
"""

from dataclasses import dataclass
from core.complexity import classify_complexity

@dataclass
class ExecutionPlan:

    intent: str

    complexity: str

    capability: str

    model: str | None

    tool: str | None

    memory: bool

    browser: bool

    image_generation: bool

    vision: bool

from core.registry import REGISTRY

FAST = "FAST_GENERAL"
DEEP = "DEEP_REASONING"
CODE = "CODING"
DOC = "DOCUMENT_QA"


def build_plan(intent, user_input):
    complexity = classify_complexity(user_input)
    if intent == "GENERAL":

        if complexity == "HIGH":
            capability = DEEP
        else:
            capability = FAST

        return ExecutionPlan(
            intent=intent,
	    complexity=complexity,
	    capability=capability,
            model=REGISTRY[capability]["model"],
            tool=REGISTRY[capability]["tool"],
            memory=False,
            browser=False,
            image_generation=False,
            vision=False,
        )

    elif intent == "CODING":

        return ExecutionPlan(
            intent=intent,
	    complexity=complexity,
	    capability="CODING",
            model=REGISTRY["CODING"]["model"],
            tool=REGISTRY["CODING"]["tool"],
            memory=False,
            browser=False,
            image_generation=False,
            vision=False,
        )

    elif intent == "DOCUMENT":

        return ExecutionPlan(
	    intent=intent,
	    complexity=complexity,
	    capability="DOCUMENT_QA",
	    model=REGISTRY["DOCUMENT_QA"]["model"],
	    tool=REGISTRY["DOCUMENT_QA"]["tool"],
	    memory=True,
	    browser=False,
	    image_generation=False,
	    vision=False,
	)

    return ExecutionPlan(
        intent="UNKNOWN",
	complexity=complexity,
        capability="FAST_GENERAL",
        model=REGISTRY["FAST_GENERAL"]["model"],
        tool=REGISTRY["FAST_GENERAL"]["tool"],
        memory=False,
        browser=False,
        image_generation=False,
        vision=False,
    )