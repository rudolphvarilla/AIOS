"""
===========================================================
AIOS Execution Planner
core/planner/planner.py
===========================================================

Creates an execution plan from

• IntentResult
• ContextResult
• SemanticResult
• PerceptionResult

Planner is now the intelligence.

Router only translates the finished plan.

Version 4.0
===========================================================
"""

from dataclasses import dataclass, field

from core.context.overrides import DOMAIN_OVERRIDES


# ---------------------------------------------------------
# Default Route
# ---------------------------------------------------------

DEFAULT_ROUTE = {

    "model_capability": "GENERAL",

    "tool_capability": None,

    "browser": False,

    "vision": False,

    "image_generation": False,

    "repository": False,

    "memory": False,

    "profile": False,

    "workspace": False,

    "time": False,

    "longterm": False,

}


# =========================================================
# Execution Plan
# =========================================================

@dataclass
class ExecutionPlan:

    intent: str

    complexity: str

    # ---------------------------------

    context_domains: set[str]

    primary_domain: str | None

    primary_concept: str | None

    # ---------------------------------

    model_capability: str

    tool_capability: str | None

    # ---------------------------------

    perception: object | None

    # ---------------------------------

    prompt_flags: dict[str, bool]

    # ---------------------------------

    browser: bool

    vision: bool

    image_generation: bool

    # ---------------------------------

    confidence: float = 0.0

    execution_order: list[str] = field(default_factory=list)


# =========================================================
# Planner
# =========================================================

def build_plan(

    intent,

    query,

    context=None,

    perception=None,

    semantic_result=None,

):

    intent_result = intent

    route = DEFAULT_ROUTE.copy()

    # --------------------------------------------------
    # Complexity
    # --------------------------------------------------

    complexity = intent_result.complexity

    if (

        semantic_result is not None

        and getattr(semantic_result, "complexity", None)

    ):

        complexity = semantic_result.complexity

    # --------------------------------------------------
    # Context
    # --------------------------------------------------

    domains = set()

    primary_domain = None

    primary_concept = None

    if context is not None:

        domains = set(context.domains)

        primary_domain = context.primary_domain

        primary_concept = context.primary_concept

    # --------------------------------------------------
    # Intent Based Routing
    # --------------------------------------------------

    intent_name = intent_result.intent.upper()

    if intent_name in {

        "CODE",

        "PROGRAM",

        "DEBUG",

    }:

        route["model_capability"] = "CODING"

    # --------------------------------------------------
    # Domain Routing
    # --------------------------------------------------

    if primary_domain == "coding":

        route["model_capability"] = "CODING"

    elif primary_domain == "travel":

        route["browser"] = True

        route["time"] = True

    elif primary_domain == "photography":

        route["repository"] = True

    # --------------------------------------------------
    # Domain Overrides
    # --------------------------------------------------

    for domain in domains:

        overrides = DOMAIN_OVERRIDES.get(domain)

        if overrides:

            route.update(overrides)

    # --------------------------------------------------
    # Perception Overrides
    # --------------------------------------------------

    if perception is not None:

        requirement_names = {

            r.name

            for r in perception.requirements

        }

        if "recommendation" in requirement_names:

            route["browser"] = True

    # --------------------------------------------------
    # Semantic Overrides
    # --------------------------------------------------

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

        if semantic_result.requires_search:

            route["browser"] = True

        if semantic_result.requires_code:

            route["model_capability"] = "CODING"

        if semantic_result.requires_repository:

            route["repository"] = True

        if semantic_result.requires_memory:

            route["memory"] = True

        if semantic_result.requires_vision:

            route["vision"] = True

        if semantic_result.requires_image_generation:

            route["image_generation"] = True

    # --------------------------------------------------
    # Build Execution Plan
    # --------------------------------------------------

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

            if key in {

                "repository",

                "memory",

                "profile",

                "workspace",

                "time",

                "longterm",

            }

        },

        browser=route["browser"],

        vision=route["vision"],

        image_generation=route["image_generation"],

        confidence=confidence,

        execution_order=execution_order,

    )