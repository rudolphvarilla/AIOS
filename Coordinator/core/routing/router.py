"""
===========================================================
AIOS Capability Router
core/routing/router.py
===========================================================

Version 4

The router no longer interprets the user request.

It only converts an ExecutionPlan into executable routing
instructions.

The Planner is now the intelligence.

The Router is only the translator.

===========================================================
"""

from core.routing.routes import DEFAULT_ROUTE


class CapabilityRouter:

    def route(self, plan):

        route = DEFAULT_ROUTE.copy()

        # ----------------------------------
        # Planner decides capabilities
        # ----------------------------------

        route["model_capability"] = plan.model_capability
        route["tool_capability"] = plan.tool_capability

        # ----------------------------------
        # Planner decides prompt sources
        # ----------------------------------

        route.update(plan.prompt_flags)

        # ----------------------------------
        # Planner decides execution flags
        # ----------------------------------

        route["browser"] = plan.browser
        route["vision"] = plan.vision
        route["image_generation"] = plan.image_generation

        return route