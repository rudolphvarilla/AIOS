"""
===========================================================
AIOS Decision Engine
core/decision/engine.py
===========================================================

Determines which services execute before the model.

Decision Engine v4

Uses semantic domains produced by the Context Engine.

Version
4.0
===========================================================
"""

from dataclasses import dataclass

from core.decision.rules import DOMAIN_RULES


@dataclass
class Decision:

    use_search: bool

    background: bool

    reasoning: str


class DecisionEngine:

    def __init__(self):

        pass

    def decide(
        self,
        prompt: str,
        context=None,
        plan=None,
):

        prompt_lower = prompt.lower()

        # ---------------------------------
        # No semantic context
        # ---------------------------------

        if context is None:

            return Decision(

                use_search=False,

                background=False,

                reasoning="No semantic context."

            )

        # ---------------------------------
        # Evaluate semantic domains
        # ---------------------------------

        for domain in context.domains:

            rule = DOMAIN_RULES.get(domain)

            if rule is None:

                continue

            search = rule["search"]

            # -----------------------------
            # Always Search
            # -----------------------------

            if search is True:

                return Decision(

                    use_search=True,

                    background=rule["background"],

                    reasoning=rule["reason"]

                )

            # -----------------------------
            # Never Search
            # -----------------------------

            if search is False:

                return Decision(

                    use_search=False,

                    background=rule["background"],

                    reasoning=rule["reason"]

                )

            # -----------------------------
            # Conditional Search
            # -----------------------------

            if search == "conditional":

                if self._needs_live_information(prompt_lower):

                    return Decision(

                        use_search=True,

                        background=rule["background"],

                        reasoning=rule["reason"]

                    )

                return Decision(

                    use_search=False,

                    background=rule["background"],

                    reasoning=f"{domain.capitalize()} handled locally."

                )

        # ---------------------------------
        # Execution Plan Overrides
        # ---------------------------------

        if plan is not None:

            if plan.browser:

                return Decision(

                    use_search=True,

                    background=False,

                    reasoning="Execution plan requests browser capability."

                )

        # ---------------------------------
        # Default
        # ---------------------------------

        return Decision(

            use_search=False,

            background=False,

            reasoning="General knowledge question."

        )

    # ==================================================
    # Helper
    # ==================================================

    def _needs_live_information(self, prompt: str):

        LIVE_TERMS = (

            "today",
            "current",
            "latest",
            "recent",
            "now",
            "price",
            "schedule",
            "available",
            "availability",
            "news",
            "status",
            "forecast",
            "exchange rate",
            "flight",
            "hotel"

        )

        return any(term in prompt for term in LIVE_TERMS)