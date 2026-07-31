"""
===========================================================
AIOS Semantic Understanding
core/intent/llm_understanding.py
===========================================================

Uses a lightweight reasoning model to understand the
true intent of the user's request before symbolic routing.

Responsibilities

• Infer semantic domains
• Infer concepts
• Infer entities
• Infer requirements
• Decide execution hints
• Estimate complexity
• Produce structured semantic output

Version 2.0
===========================================================
"""

import json
import re

from core.semantics.result import SemanticResult

SCHEMA = """
{
  "domains": [],
  "concepts": [],
  "entities": [],
  "requirements": [],

  "normalized_query": "",
  "search_query": "",
  "search_intent": "",

  "needs_search": false,
  "ambiguity": 0.0,

  "complexity":"LOW",

  "requires_search":false,
  "requires_code":false,
  "requires_memory":false,
  "requires_repository":false,
  "requires_vision":false,
  "requires_image_generation":false,

  "confidence":0.0,

  "execution_order":[]
}
"""

class SemanticUnderstanding:

    def __init__(self, model_manager):

        self.model_manager = model_manager

    # -----------------------------------------------------

    def understand(

        self,

        query,

        repository=None,

        memory=None,

    ):

        config = self.model_manager.get("qwen2.5:1.5b")

        if config is None:

            return self.empty_result()

        model = config.wrapper

        # Build prompt
        prompt = self.build_prompt(query)

        # Execute model
        raw = model.generate(prompt)

        return self.parse(raw)

    # -----------------------------------------------------

    def build_prompt(self, query):

        return f"""
You are AIOS Semantic Understanding.

Read the user's request.

Your job is NOT to answer.

Return ONLY valid JSON.

Schema

{SCHEMA}

Definitions

domains
High-level knowledge domains (travel, photography, coding, finance, aviation, etc.)

concepts
Important concepts inside the domains.

entities
Specific people, places, products, organizations, or named objects.

requirements
What the user is asking for (recommendation, comparison, explanation, booking, troubleshooting, etc.)

normalized_query
Rewrite the user's request into clear English.

search_query
Rewrite the request exactly as a search engine should receive it.

search_intent
One concise sentence describing the user's true information need.

needs_search
True if external information is required.

ambiguity
0.0 = perfectly clear
1.0 = impossible to understand

Return ONLY valid JSON.

User

{query}
"""

    # -----------------------------------------------------

    def parse(self, raw):

        try:

            cleaned = self.clean_json(raw)

            data = json.loads(cleaned)

        except Exception:

            return SemanticResult.empty()

        return SemanticResult.from_dict(data)

    # -----------------------------------------------------

    def clean_json(self, text):

        text = re.sub(
            r"```json|```",
            "",
            text,
            flags=re.IGNORECASE,
        )

        start = text.find("{")

        end = text.rfind("}")

        if start == -1 or end == -1:

            return "{}"

        return text[start:end + 1]

    # -----------------------------------------------------

    def empty_result(self):

        return SemanticResult.empty()