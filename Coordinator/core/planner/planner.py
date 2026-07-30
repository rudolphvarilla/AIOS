"""
===========================================================
AIOS Execution Planner
core/planner/planner.py
===========================================================

Creates an execution plan from:

• IntentResult
• Semantic Context
• Semantic Understanding
• Routing Rules

Planner does NOT call any LLM.

Version 2.0
===========================================================
"""

from dataclasses import dataclass, field

from core.routing.router import CapabilityRouter
from core.context.overrides import DOMAIN_OVERRIDES
from core.intent.result import IntentResult

router = CapabilityRouter()


@dataclass
class ExecutionPlan:

    intent: str

    complexity: str

    # ---------------------------------
    # Semantic Context
    # ---------------------------------

    context_domains: set[str]

    primary_domain: str | None

    primary_concept: str | None

    # ---------------------------------
    # Routing
    # ---------------------------------

    model_capability: str

    tool_capability: str | None

    # ---------------------------------
    # Perception
    # ---------------------------------

    perception: object | None

    # ---------------------------------
    # Prompt Planning
    # ---------------------------------

    prompt_flags: dict[str, bool]

    # ---------------------------------
    # Execution
    # ---------------------------------

    browser: bool

    image_generation: bool

    vision: bool

    # ---------------------------------
    # Tiny reasoning output
    # ---------------------------------

    confidence: float = 0.0

    execution_order: list[str] = field(default_factory=list)


# ==========================================================
# Build Plan
# ==========================================================

def build_plan(
    intent_result: IntentResult,
    context=None,
    perception=None,
    semantic_result=None,
):

    # ---------------------------------
    # Complexity
    # ---------------------------------

    complexity = intent_result.complexity

    if semantic_result is not None:

        if getattr(semantic_result, "complexity", None):

            complexity = semantic_result.complexity

    # ---------------------------------
    # Semantic Context
    # ---------------------------------

    domains = set()

    primary_domain = None

    primary_concept = None

    if context is not None:

        domains = context.domains

        primary_domain = context.primary_domain

        primary_concept = context.primary_concept

    # ---------------------------------
    # Base Routing
    # ---------------------------------

    route = router.route(

        intent_result.intent,

        complexity,

        "",

    )

    # ---------------------------------
    # Domain Routing
    # ---------------------------------

    if primary_domain == "coding":

        route["model_capability"] = "CODING"

    elif primary_domain == "photography":

        route["repository"] = True

    elif primary_domain == "travel":

        route["time"] = True

    # ---------------------------------
    # Domain Overrides
    # ---------------------------------

    for domain in domains:

        overrides = DOMAIN_OVERRIDES.get(domain)

        if overrides:

            route.update(overrides)

    # ---------------------------------
    # Perception Overrides
    # ---------------------------------

    if perception is not None:

        requirement_names = {

            r.name

            for r in perception.requirements

        }

        if "recommendation" in requirement_names:

            route["browser"] = True

    # ---------------------------------
    # Tiny LLM Overrides
    # ---------------------------------

    confidence = 0.0

    execution_order = []

    if semantic_result is not None:

        confidence = getattr(

            semantic_result,

            "confidence",

            0.0,

        )

        execution_order = getattr(

            semantic_result,

            "execution_order",

            [],

        )

        if getattr(

            semantic_result,

            "requires_search",

            False,

        ):

            route["browser"] = True

        if getattr(

            semantic_result,

            "requires_code",

            False,

        ):

            route["model_capability"] = "CODING"

        if getattr(

            semantic_result,

            "requires_vision",

            False,

        ):

            route["vision"] = True

        if getattr(

            semantic_result,

            "requires_image_generation",

            False,

        ):

            route["image_generation"] = True

    # ---------------------------------
    # Build Plan
    # ---------------------------------

    return ExecutionPlan(

        intent=intent_result.intent,

        complexity=complexity,

        context_domains=domains,

        primary_domain=primary_domain,

        primary_concept=primary_concept,

        model_capability=route["model_capability"],

        tool_capability=route["tool_capability"],

        perception=perception,

        prompt_flags={

            key: value

            for key, value in route.items()

            if key in (

                "repository",

                "memory",

                "profile",

                "workspace",

                "time",

                "longterm",

            )

        },

        browser=route["browser"],

        image_generation=route["image_generation"],

        vision=route["vision"],

        confidence=confidence,

        execution_order=execution_order,

    )