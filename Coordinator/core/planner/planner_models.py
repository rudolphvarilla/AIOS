"""
===========================================================
AIOS Planner Models
core/planner/planner_models.py
===========================================================

Provides the reasoning model used by the AIOS Planner.

The planner is completely isolated from the Coordinator.

Future

- Ollama
- OpenAI
- Claude
- Gemini
- AnythingLLM

Version 1.0
===========================================================
"""

from core.models.model import Model


class PlannerModel:

    def __init__(self):

        self.model = Model()

        # ---------------------------------------
        # Temporary planner model
        # ---------------------------------------

        self.model_name = "qwen2.5:1.5b"

    # ==================================================

    def generate(self, prompt: str):

        """
        Execute planner reasoning.

        Returns

        Raw string returned by the model.
        """

        return self.model.generate(

            prompt=prompt,

            model=self.model_name,

        )