"""
===========================================================
AIOS Capability Router
core/routing/router.py
===========================================================

Version 4.1

The router primarily converts an ExecutionPlan into executable
routing instructions. A small legacy compatibility path is kept
for older smoke scripts that still call route(intent, complexity).
===========================================================
"""

from core.routing.routes import DEFAULT_ROUTE, ROUTES


class CapabilityRouter:

    def route(self, plan, complexity=None):
        # Legacy compatibility: older callers passed intent and complexity.
        # The Planner remains the source of truth for normal execution.
        if isinstance(plan, str):
            route = ROUTES.get(plan, DEFAULT_ROUTE).copy()
            return route

        route = DEFAULT_ROUTE.copy()

        route["model_capability"] = plan.model_capability
        route["tool_capability"] = plan.tool_capability
        route.update(plan.prompt_flags)
        route["browser"] = plan.browser
        route["vision"] = plan.vision
        route["image_generation"] = plan.image_generation

        return route
